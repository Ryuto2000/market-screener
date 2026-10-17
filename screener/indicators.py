"""Pure-pandas indicator logic for the momentum screener (see README for the rules).

Every function takes a daily OHLCV DataFrame with columns
Open, High, Low, Close, Volume (ascending DatetimeIndex) and returns plain values,
so the logic can be unit-tested without network access.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, asdict

import pandas as pd

LOOKBACK_3M = 63      # trading days ≈ 3 months
LOOKBACK_52W = 252
LOOKBACK_6M = 126
MIN_ROWS = 220        # 200MA + 20-day slope; also excludes IPO < ~200 trading days
BREAKOUT_WINDOW = 3   # breakout must be within the last 3 sessions
BREAKOUT_VOL_MULT = 1.5
CHASE_LIMIT = 0.03
NEAR_HIGH = 0.03
PULLBACK_WINDOW = 20  # breakout within the last ~4 weeks
PULLBACK_BAND = 0.03
MAX_STOP_DIST = 0.15


@dataclass
class Metrics:
    ok: bool
    reason: str = ""
    date: str = ""
    close: float = math.nan
    sma20: float = math.nan
    sma50: float = math.nan
    sma200: float = math.nan
    sma200_20ago: float = math.nan
    high_52w: float = math.nan
    high_3m: float = math.nan
    pct_from_52w_high: float = math.nan
    ret_6m: float = math.nan
    rs_raw: float = math.nan  # IBD-style weighted return: 0.4*3m + 0.2*(6m + 9m + 12m)
    vol_ratio: float = math.nan
    turnover_20d: float = math.nan
    trend_ok: bool = False
    trend_detail: dict = field(default_factory=dict)
    triggers: list = field(default_factory=list)
    breakout_level: float | None = None
    breakout_date: str | None = None
    entry_limit: float | None = None
    chase_ok: bool | None = None
    stop_8pct: float = math.nan
    stop_struct: float | None = None
    stop_struct_dist: float | None = None
    flags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        for k, v in list(d.items()):
            if isinstance(v, float):
                d[k] = None if math.isnan(v) else round(v, 4)
        return d


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
    df = df.dropna(subset=["Close"])
    df = df[df["Close"] > 0]
    return df.sort_index()


def _find_breakout(df: pd.DataFrame, within: int, need_volume: bool) -> tuple[int, float] | None:
    """Most recent session i in the last `within` sessions whose close exceeds the
    highest High of the 63 sessions before it. Returns (position, level)."""
    n = len(df)
    vol50 = df["Volume"].rolling(50).mean().shift(1)
    prior_high = df["High"].rolling(LOOKBACK_3M).max().shift(1)
    for i in range(n - 1, max(n - 1 - within, LOOKBACK_3M) , -1):
        level = prior_high.iloc[i]
        if pd.isna(level):
            continue
        if df["Close"].iloc[i] > level:
            if need_volume:
                v50 = vol50.iloc[i]
                if pd.isna(v50) or v50 <= 0 or df["Volume"].iloc[i] < BREAKOUT_VOL_MULT * v50:
                    continue
            return i, float(level)
    return None


def compute(df: pd.DataFrame, bench_ret_6m: float | None) -> Metrics:
    df = _clean(df)
    if len(df) < MIN_ROWS:
        return Metrics(ok=False, reason=f"rows<{MIN_ROWS} (IPO or missing data)")

    c = df["Close"]
    m = Metrics(ok=True)
    m.date = str(df.index[-1].date())
    m.close = float(c.iloc[-1])
    sma20 = c.rolling(20).mean()
    sma50 = c.rolling(50).mean()
    sma200 = c.rolling(200).mean()
    m.sma20, m.sma50, m.sma200 = float(sma20.iloc[-1]), float(sma50.iloc[-1]), float(sma200.iloc[-1])
    m.sma200_20ago = float(sma200.iloc[-21])
    m.high_52w = float(df["High"].iloc[-LOOKBACK_52W:].max())
    m.high_3m = float(df["High"].iloc[-LOOKBACK_3M:].max())
    m.pct_from_52w_high = m.close / m.high_52w - 1
    m.ret_6m = m.close / float(c.iloc[-LOOKBACK_6M - 1]) - 1
    rets = [m.close / float(c.iloc[-n - 1]) - 1 if len(c) > n else m.ret_6m for n in (63, 126, 189, 252)]
    m.rs_raw = 0.4 * rets[0] + 0.2 * (rets[1] + rets[2] + rets[3])
    v50 = df["Volume"].iloc[-51:-1].mean()
    m.vol_ratio = float(df["Volume"].iloc[-1] / v50) if v50 > 0 else math.nan
    m.turnover_20d = float((df["Close"] * df["Volume"]).iloc[-20:].mean())

    td = {
        "sma50_gt_sma200": m.sma50 > m.sma200,
        "close_gt_sma50": m.close > m.sma50,
        "sma200_rising": m.sma200 > m.sma200_20ago,
        "within_15pct_of_52w_high": m.pct_from_52w_high >= -0.15,
        "rs_beats_benchmark": (bench_ret_6m is not None and m.ret_6m > bench_ret_6m),
    }
    m.trend_detail = td
    m.trend_ok = all(td.values())

    # --- triggers -------------------------------------------------------
    n = len(df)
    bo = _find_breakout(df, BREAKOUT_WINDOW, need_volume=True)
    if bo:
        i, level = bo
        m.triggers.append("a_breakout")
        m.breakout_level, m.breakout_date = level, str(df.index[i].date())
        m.entry_limit = level * (1 + CHASE_LIMIT)
        m.chase_ok = m.close <= m.entry_limit

    if m.close >= m.high_3m * (1 - NEAR_HIGH) and "a_breakout" not in m.triggers:
        m.triggers.append("b_near_high")
        m.entry_limit = m.high_3m * (1 + CHASE_LIMIT)
        m.chase_ok = True  # entry is a buy-stop just above the high

    # (c) pullback re-entry: breakout 4..20 sessions ago (volume not required),
    # then a dip to the breakout level or 20MA (±3%), and today closes up.
    pb = _find_breakout(df.iloc[: n - BREAKOUT_WINDOW], PULLBACK_WINDOW - BREAKOUT_WINDOW, need_volume=False)
    if pb and "a_breakout" not in m.triggers:
        i, level = pb
        after = df.iloc[i + 1:]
        if len(after) >= 2:
            low_pos = int(after["Low"].values.argmin())
            dip_low = float(after["Low"].iloc[low_pos])
            ref_sma20 = float(sma20.iloc[i + 1 + low_pos])
            touched = (abs(dip_low / level - 1) <= PULLBACK_BAND) or (abs(dip_low / ref_sma20 - 1) <= PULLBACK_BAND)
            rebound = (m.close > float(c.iloc[-2])) and (m.close > float(df["Open"].iloc[-1])) and low_pos < len(after) - 1
            if touched and rebound:
                m.triggers.append("c_pullback")
                if "b_near_high" not in m.triggers:  # near the high: the buy-stop above it is the entry
                    m.breakout_level, m.breakout_date = level, str(df.index[i].date())
                    m.entry_limit = dip_low * (1 + CHASE_LIMIT)
                    m.chase_ok = m.close <= m.entry_limit

    # --- stops ------------------------------------------------------------
    m.stop_8pct = m.close * 0.92
    supports = [x for x in (m.sma20, m.breakout_level) if x is not None and x < m.close]
    if supports:
        m.stop_struct = max(supports) * 0.99
        m.stop_struct_dist = 1 - m.stop_struct / m.close
        if m.stop_struct_dist > MAX_STOP_DIST:
            m.flags.append("wide_stop")
    if m.vol_ratio and m.vol_ratio > 5:
        m.flags.append("volume_spike_5x")
    return m


def benchmark_ret_6m(df: pd.DataFrame) -> float | None:
    df = _clean(df)
    if len(df) <= LOOKBACK_6M:
        return None
    c = df["Close"]
    return float(c.iloc[-1] / c.iloc[-LOOKBACK_6M - 1] - 1)

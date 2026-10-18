"""Replay the screener on past data and follow every breakout signal forward.

For each trading day in the history, a stock gives a signal when the screener would have shown it
as an "a_breakout" A-candidate that day: liquid, trend template passed, 6-month return above the
benchmark, close above the prior 3-month high on >= 1.5x the 50-day volume, and close within the
chase limit (breakout level + 3%). The trade is entered at the next session's open (a market order
placed after the close) and followed with simulate.follow().

Not modelled: market cap, fundamentals, earnings dates and theme/crypto exclusions (no
point-in-time data). The universe is today's listing, so delisted stocks are missing
(survivorship bias: results are somewhat optimistic).

Usage: python -m screener.backtest --market jp [--years 5]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import indicators as ind
from . import rules, simulate, stats
from .fetch import download
from .run import CFG
from .universe import jp_universe, us_universe

OUT = Path("data/eval")
REFRACTORY = 20  # ignore a new signal on the same stock within 20 sessions of the last one


def log(*a):
    print(dt.datetime.now().strftime("%H:%M:%S"), *a, file=sys.stderr, flush=True)


def _rs_raw(c: pd.Series) -> pd.Series:
    r = {n: c / c.shift(n) - 1 for n in (63, 126, 189, 252)}
    return 0.4 * r[63] + 0.2 * (r[126] + r[189].fillna(r[126]) + r[252].fillna(r[126]))


def candidate_days(df: pd.DataFrame, bench6m: pd.Series, min_turnover: float) -> pd.Series:
    """Boolean Series: days that pass liquidity, trend, RS, breakout-with-volume and the chase limit."""
    c, h, v = df["Close"], df["High"], df["Volume"]
    s50, s200 = c.rolling(50).mean(), c.rolling(200).mean()
    hi52 = h.rolling(ind.LOOKBACK_52W, min_periods=200).max()
    prior63 = h.rolling(ind.LOOKBACK_3M).max().shift(1)
    vol50 = v.rolling(50).mean().shift(1)
    turn20 = (c * v).rolling(20).mean()
    ret6m = c / c.shift(ind.LOOKBACK_6M) - 1
    b6 = bench6m.reindex(df.index).ffill()
    rows = pd.Series(np.arange(1, len(df) + 1), index=df.index)
    trend = (s50 > s200) & (c > s50) & (s200 > s200.shift(20)) & (c >= hi52 * 0.85) & (ret6m > b6)
    breakout = (c > prior63) & (v >= ind.BREAKOUT_VOL_MULT * vol50) & (c <= prior63 * (1 + ind.CHASE_LIMIT))
    return (rows >= ind.MIN_ROWS) & (turn20 >= min_turnover) & trend & breakout


def regime_series(bench: pd.DataFrame) -> pd.DataFrame:
    c, v = bench["Close"], bench["Volume"]
    s50, s200 = c.rolling(50).mean(), c.rolling(200).mean()
    state = np.where((c > s50) & (s50 > s200), "uptrend",
                     np.where((c < s200) & (s50 < s200), "downtrend", "mixed"))
    dd = ((c.pct_change() <= -0.002) & (v > v.shift(1))).astype(int).rolling(25).sum()
    return pd.DataFrame({"regime_state": state, "dist_days": dd}, index=bench.index)


def main(market: str, years: int) -> int:
    cfg = CFG[market]
    uni = jp_universe() if market == "jp" else us_universe()
    log(f"universe: {len(uni)}")
    bench = download([cfg["bench"]], period=f"{years}y", auto_adjust=False, intraday=False)[cfg["bench"]]
    bench = ind._clean(bench)
    bench6m = bench["Close"] / bench["Close"].shift(ind.LOOKBACK_6M) - 1
    regime = regime_series(bench)
    # benchmark opening gap on each session (open vs previous close): the entry day's market mood
    bench_gap = bench["Open"] / bench["Close"].shift(1) - 1
    prices = download(uni["ticker"].tolist(), period=f"{years}y", auto_adjust=False, intraday=False)
    prices = {t: ind._clean(df) for t, df in prices.items() if df is not None and len(df) > ind.MIN_ROWS + 5}
    log(f"with history: {len(prices)}")

    # cross-sectional RS rating per day among liquid names
    raw, liquid = {}, {}
    for t, df in prices.items():
        raw[t] = _rs_raw(df["Close"])
        liquid[t] = (df["Close"] * df["Volume"]).rolling(20).mean() >= cfg["min_turnover"]
    raw = pd.DataFrame(raw)
    raw = raw.where(pd.DataFrame(liquid).reindex(raw.index).fillna(False).astype(bool))
    rs_rating = (raw.rank(axis=1, pct=True) * 98 + 1).round()
    breadth = (pd.DataFrame({t: df["Close"] > df["Close"].rolling(50).mean() for t, df in prices.items()})
               .where(raw.notna()).mean(axis=1))

    names = uni.set_index("ticker")["name"].to_dict() if "name" in uni else {}
    events = []
    for k, (t, df) in enumerate(prices.items()):
        days = candidate_days(df, bench6m, cfg["min_turnover"])
        last_i = -10 ** 9
        for i in np.flatnonzero(days.to_numpy()):
            if i - last_i < REFRACTORY or i + 1 >= len(df):
                continue
            last_i = i
            d = df.index[i]
            b6 = float(bench6m.reindex([d]).iloc[0]) if d in bench6m.index else None
            m = ind.compute(df.iloc[: i + 1], b6)
            ev = {"ticker": t, "name": names.get(t), "signal_date": str(d.date()), "close": round(float(df["Close"].iloc[i]), 2),
                  "rs_rating": float(rs_rating.at[d, t]) if d in rs_rating.index and not pd.isna(rs_rating.at[d, t]) else None,
                  "flags": [f for f in m.flags if f not in ("fin_unknown",)], "plus": list(m.plus),
                  "rsi14": m.rsi14, "atr_pct": m.atr_pct, "base_depth": m.base_depth, "updown_vol_50": m.updown_vol_50,
                  "vol_ratio": m.vol_ratio, "breadth50": float(breadth.get(d, np.nan))}
            if d in regime.index:
                ev["regime_state"] = str(regime.at[d, "regime_state"])
                ev["dist_days"] = float(regime.at[d, "dist_days"]) if not pd.isna(regime.at[d, "dist_days"]) else None
            ed = df.index[i + 1]
            ev["bench_gap"] = float(bench_gap.get(ed, np.nan))
            ev["stock_gap"] = float(df["Open"].iloc[i + 1] / df["Close"].iloc[i] - 1)
            ev.update(simulate.follow(df, i + 1))
            events.append(ev)
        if (k + 1) % 500 == 0:
            log(f"scanned {k + 1}/{len(prices)}; signals {len(events)}")
    log(f"signals: {len(events)}")

    ev = pd.DataFrame(events)
    OUT.mkdir(parents=True, exist_ok=True)
    if len(ev):
        ev["passes_rules"] = [rules.check(market, r, {"benchmark_state": r.get("regime_state"),
                                                       "benchmark_distribution_days_25": r.get("dist_days")})[0]
                              for r in ev.to_dict("records")]
    res = {"all_signals": stats.breakdown(ev),
           "with_rules": stats.breakdown(ev[ev["passes_rules"]]) if len(ev) else {}}
    span = (ev["signal_date"].min(), ev["signal_date"].max()) if len(ev) else (None, None)
    notes = [f"market: {market}, signals from {span[0]} to {span[1]}, entry at the next open after the signal day",
             "rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions",
             "survivorship bias: today's listings only, so results lean optimistic",
             "'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)"]
    meta = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "market": market,
            "years": years, "signals": len(ev), "span": span, "notes": notes}
    (OUT / f"backtest_{market}.json").write_text(json.dumps({**meta, "results": res}, ensure_ascii=False, indent=1, default=str))
    md = stats.markdown(f"Backtest {market.upper()}: signals that pass the current rules (screener/rules.py)", res["with_rules"], notes)
    md += "\n\n" + stats.markdown(f"Backtest {market.upper()}: all breakout signals (before the market rules)", res["all_signals"], [])
    (OUT / f"backtest_{market}.md").write_text(md)
    if len(ev):
        ev.drop(columns=[c for c in ("name",) if c in ev]).to_csv(OUT / f"backtest_events_{market}.csv", index=False)
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    p.add_argument("--years", type=int, default=5)
    a = p.parse_args()
    sys.exit(main(a.market, a.years))

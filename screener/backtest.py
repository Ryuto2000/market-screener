"""Replay the screener on past data and follow every breakout signal forward.

Three entry types are replayed: (a) breakout (below), (b) near the 3-month high (bought at the next
open, and separately with a buy-stop just above the high within 5 sessions), (c) pullback re-entry.
The main tables use (a); a comparison table covers all types.

For each trading day in the history, a stock gives an (a) signal when the screener would have shown it
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
from . import earnings, rules, simulate, stats
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


def _base_masks(df: pd.DataFrame, bench6m: pd.Series, min_turnover: float):
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
    base = (rows >= ind.MIN_ROWS) & (turn20 >= min_turnover) & trend
    brk_vol = (c > prior63) & (v >= ind.BREAKOUT_VOL_MULT * vol50)
    return base, prior63, brk_vol


def candidate_days(df: pd.DataFrame, bench6m: pd.Series, min_turnover: float) -> pd.Series:
    """(a) breakout: days that pass liquidity, trend, RS, breakout-with-volume and the chase limit."""
    base, prior63, brk_vol = _base_masks(df, bench6m, min_turnover)
    return base & brk_vol & (df["Close"] <= prior63 * (1 + ind.CHASE_LIMIT))


def near_high_days(df: pd.DataFrame, bench6m: pd.Series, min_turnover: float) -> pd.Series:
    """(b) within 3% under the 3-month high (incl. today), not above the prior high, and no
    volume breakout in the last 3 sessions (as the live screener's b_near_high)."""
    base, prior63, brk_vol = _base_masks(df, bench6m, min_turnover)
    hi63 = df["High"].rolling(ind.LOOKBACK_3M).max()
    recent_a = brk_vol.astype(int).rolling(ind.BREAKOUT_WINDOW).max().fillna(0).astype(bool)
    c = df["Close"]
    return base & (c >= hi63 * (1 - ind.NEAR_HIGH)) & (c <= prior63) & ~recent_a


def pullback_days(df: pd.DataFrame, bench6m: pd.Series, min_turnover: float) -> pd.Series:
    """(c) pullback re-entry as in the live screener: a close above the prior 3-month high 4..20 sessions
    ago, a later low within 3% of that level or of the 20-day SMA, and today an up close above the open."""
    base, prior63, brk_vol = _base_masks(df, bench6m, min_turnover)
    c, o, l = (df[k].to_numpy(float) for k in ("Close", "Open", "Low"))
    p63 = prior63.to_numpy(float)
    s20 = df["Close"].rolling(20).mean().to_numpy(float)
    brk = c > p63
    recent_a = brk_vol.astype(int).rolling(ind.BREAKOUT_WINDOW).max().fillna(0).astype(bool).to_numpy()
    ok = base.to_numpy()
    out = np.zeros(len(df), bool)
    for t in np.flatnonzero(ok & ~recent_a):
        if t < 1 or not (c[t] > c[t - 1] and c[t] > o[t]):
            continue
        lo, hi = t - ind.PULLBACK_WINDOW, t - ind.BREAKOUT_WINDOW - 1
        ks = np.flatnonzero(brk[max(lo, 0):hi + 1])
        if not len(ks):
            continue
        k = max(lo, 0) + ks[-1]
        level = p63[k]
        seg = l[k + 1:t]
        if len(seg) < 1:
            continue
        j = k + 1 + int(seg.argmin())
        dip = l[j]
        touched = abs(dip / level - 1) <= ind.PULLBACK_BAND or (not np.isnan(s20[j]) and abs(dip / s20[j] - 1) <= ind.PULLBACK_BAND)
        if touched and c[t] <= dip * (1 + ind.CHASE_LIMIT):
            out[t] = True
    return pd.Series(out, index=df.index)


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
    # drop broken histories (e.g. delisted names with garbage prices): any daily move beyond +200% / -90%
    bad = [t for t, df in prices.items() if ((df["Close"].pct_change() > 2) | (df["Close"].pct_change() < -0.9)).any()]
    for t in bad:
        prices.pop(t)
    if bad:
        log(f"dropped {len(bad)} tickers with broken price history")
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

    def record(t, df, i, kind, entry_i, entry_px=None, edays=None):
        d = df.index[i]
        b6 = float(bench6m.reindex([d]).iloc[0]) if d in bench6m.index else None
        m = ind.compute(df.iloc[: i + 1], b6)
        ev = {"ticker": t, "name": names.get(t), "trigger": kind, "signal_date": str(d.date()),
              "close": round(float(df["Close"].iloc[i]), 2),
              "rs_rating": float(rs_rating.at[d, t]) if d in rs_rating.index and not pd.isna(rs_rating.at[d, t]) else None,
              "flags": [f for f in m.flags if f not in ("fin_unknown",)], "plus": list(m.plus),
              "rsi14": m.rsi14, "atr_pct": m.atr_pct, "base_depth": m.base_depth, "updown_vol_50": m.updown_vol_50,
              "vol_ratio": m.vol_ratio, "breadth50": float(breadth.get(d, np.nan))}
        if d in regime.index:
            ev["regime_state"] = str(regime.at[d, "regime_state"])
            ev["dist_days"] = float(regime.at[d, "dist_days"]) if not pd.isna(regime.at[d, "dist_days"]) else None
        ed = df.index[entry_i]
        ev["bench_gap"] = float(bench_gap.get(ed, np.nan))
        ev["stock_gap"] = float(df["Open"].iloc[entry_i] / df["Close"].iloc[entry_i - 1] - 1)
        ev.update(simulate.follow(df, entry_i, entry_px, edays))
        events.append(ev)

    for k, (t, df) in enumerate(prices.items()):
        n = len(df)
        hi63 = df["High"].rolling(ind.LOOKBACK_3M).max().to_numpy(float)
        edays = earnings.reaction_days(df, market)
        for kind, fn in (("a_breakout", candidate_days), ("b_near_high", near_high_days), ("c_pullback", pullback_days)):
            days = fn(df, bench6m, cfg["min_turnover"])
            last_i = -10 ** 9
            for i in np.flatnonzero(days.to_numpy()):
                if i - last_i < REFRACTORY or i + 1 >= n:
                    continue
                last_i = i
                record(t, df, i, kind, i + 1, edays=edays)
                if kind == "b_near_high":
                    # the same setup bought with a buy-stop just above the 3-month high within 5 sessions
                    level = hi63[i] * 1.001
                    for j in range(i + 1, min(n, i + 6)):
                        if df["High"].iloc[j] >= level:
                            record(t, df, i, "b_near_high_stop", j, max(float(df["Open"].iloc[j]), level), edays)
                            break
        if (k + 1) % 500 == 0:
            log(f"scanned {k + 1}/{len(prices)}; signals {len(events)}")
    log(f"signals: {len(events)}")

    ev = pd.DataFrame(events)
    OUT.mkdir(parents=True, exist_ok=True)
    if len(ev):
        ev["passes_rules"] = [rules.check(market, r, {"benchmark_state": r.get("regime_state"),
                                                       "benchmark_distribution_days_25": r.get("dist_days")})[0]
                              for r in ev.to_dict("records")]
    trig = {k: stats.summarize(g[g["passes_rules"]]) for k, g in ev.groupby("trigger")} if len(ev) else {}
    by_year_trig = {k: {str(y): stats.summarize(gy) for y, gy in g[g["passes_rules"]].groupby(g["signal_date"].str[:4])}
                    for k, g in ev.groupby("trigger")} if len(ev) else {}
    ev_all = ev
    ev = ev[ev["trigger"] == "a_breakout"] if len(ev) else ev
    res = {"all_signals": stats.breakdown(ev),
           "with_rules": stats.breakdown(ev[ev["passes_rules"]]) if len(ev) else {},
           "by_trigger_with_rules": trig, "by_trigger_year_with_rules": by_year_trig}
    span = (ev["signal_date"].min(), ev["signal_date"].max()) if len(ev) else (None, None)
    notes = [f"market: {market}, signals from {span[0]} to {span[1]}, entry at the next open after the signal day",
             "rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions",
             "survivorship bias: today's listings only, so results lean optimistic",
             "'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)",
             "earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher"]
    meta = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "market": market,
            "years": years, "signals": len(ev), "span": span, "notes": notes}
    (OUT / f"backtest_{market}.json").write_text(json.dumps({**meta, "results": res}, ensure_ascii=False, indent=1, default=str))
    md = stats.markdown(f"Backtest {market.upper()}: signals that pass the current rules (screener/rules.py)", res["with_rules"], notes)
    md += "\n\n" + stats.trigger_table(trig, by_year_trig)
    md += "\n\n" + stats.markdown(f"Backtest {market.upper()}: all breakout signals (before the market rules)", res["all_signals"], [])
    (OUT / f"backtest_{market}.md").write_text(md)
    if len(ev):
        ev.drop(columns=[c for c in ("name",) if c in ev]).to_csv(OUT / f"backtest_events_{market}.csv", index=False)
        ev_all.drop(columns=[c for c in ("name",) if c in ev_all]).to_csv(OUT / f"backtest_events_all_triggers_{market}.csv", index=False)
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    p.add_argument("--years", type=int, default=5)
    a = p.parse_args()
    sys.exit(main(a.market, a.years))

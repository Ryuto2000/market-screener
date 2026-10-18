"""Compare exit-rule variants on the backtest signals that pass the market rules.

Reads data/eval/backtest_events_<market>.csv (written by screener.backtest), downloads the same
price history and replays each signal with different stop widths, break-even levels and profit
targets. Writes data/eval/variants_<market>.{md,json}.

Usage: python -m screener.variants --market jp
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

import pandas as pd

from . import indicators as ind

OUT = Path("data/eval")

VARIANTS: dict[str, dict] = {
    "current: stop -8%, BE at +8%, 1/3 at +16%": {},
    "stop -6%": {"stop": 0.06},
    "stop -10%": {"stop": 0.10},
    "stop -12%": {"stop": 0.12},
    "stop -15%": {"stop": 0.15},
    "stop 3x ATR (6-12%)": {"atr_mult": 3.0},
    "BE stop at +1% (after +8%)": {"be_level": 0.01},
    "BE only after +12%": {"be_at": 0.12},
    "stop -10%, BE after +12%": {"stop": 0.10, "be_at": 0.12},
    "half at +8%, rest as current": {"trim_at": 0.08, "trim_frac": 0.5},
    "all out at +10%": {"full_at": 0.10},
    "all out at +16%": {"full_at": 0.16},
}


def run(df: pd.DataFrame, ei: int, mode: str = "intraday", stop: float = 0.08, be_at: float = 0.08,
        be_level: float = 0.0, trim_at: float = 0.16, trim_frac: float = 1 / 3, full_at: float | None = None,
        trail: float = 0.15, max_hold: int = 120, atr_mult: float | None = None, atr_pct: float | None = None,
        atr_bounds: tuple[float, float] = (0.06, 0.12)) -> tuple[float, int]:
    """Same ladder as simulate.exit_rules with every level as a parameter. Returns (return, sessions)."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    sma50 = df["Close"].rolling(50).mean().to_numpy(float)
    n, e = len(df), o[ei]
    if atr_mult is not None and atr_pct is not None and not math.isnan(atr_pct):
        stop = min(max(atr_mult * atr_pct, atr_bounds[0]), atr_bounds[1])
    sl = e * (1 - stop)
    stage, rem, real, trim, sell, hc = 0, 1.0, 0.0, False, False, e
    frac = trim_frac
    last = min(n, ei + max_hold)
    for j in range(ei, last):
        if sell:
            return real + rem * (o[j] / e - 1), j - ei
        if trim:
            real += frac * (o[j] / e - 1)
            rem -= frac
            trim = False
            if rem <= 1e-9:
                return real, j - ei
        if mode == "intraday":
            if o[j] <= sl:
                return real + rem * (o[j] / e - 1), j - ei
            if l[j] <= sl:
                return real + rem * (sl / e - 1), j - ei
        elif c[j] < sl:
            sell = True
            continue
        hc = max(hc, c[j])
        m50 = 0 if math.isnan(sma50[j]) else sma50[j]
        if full_at is not None and stage < 2 and c[j] >= e * (1 + full_at):
            trim, frac, stage = True, rem, 2
            continue
        if stage < 1 and c[j] >= e * (1 + be_at):
            sl = max(sl, e * (1 + be_level))
            stage = 1
        if stage < 2 and c[j] >= e * (1 + trim_at):
            trim, stage = True, 2
            sl = max(sl, e * (1 + trim_at / 2), m50)  # current rules: +8% after the +16% trim
        elif stage >= 2 and (j - ei) % 5 == 0:
            sl = max(sl, hc * (1 - trail), m50)
    j = last - 1
    return real + rem * (c[j] / e - 1), j - ei + 1


def _summ(g: pd.DataFrame) -> dict:
    r = g["ret"]
    w, l = r[r > 0], r[r <= 0]
    yearly = g.groupby("year")["ret"].mean()
    return {"n": int(len(r)), "win_rate": round(float((r > 0).mean()), 3),
            "not_losing_-1%": round(float((r > -0.01).mean()), 3),
            "avg_win": round(float(w.mean()), 4) if len(w) else None,
            "avg_loss": round(float(l.mean()), 4) if len(l) else None,
            "expectancy": round(float(r.mean()), 4),
            "profit_factor": round(float(w.sum() / -l.sum()), 2) if l.sum() < 0 else None,
            "days_median": float(g["days"].median()),
            "by_year": {str(k): round(float(v), 4) for k, v in yearly.items()}}


def main(market: str) -> int:
    from .fetch import download  # needs yfinance; imported here so run() is testable without it

    src = OUT / f"backtest_events_{market}.csv"
    ev = pd.read_csv(src)
    ev = ev[ev["passes_rules"]].copy()
    ev["year"] = ev["signal_date"].str[:4]
    prices = download(sorted(ev["ticker"].unique()), period="5y", auto_adjust=False, intraday=False)
    rows = []
    for _, s in ev.iterrows():
        df = prices.get(s["ticker"])
        if df is None or df.empty:
            continue
        df = ind._clean(df)
        ei = df.index.get_indexer([pd.Timestamp(s["entry_date"])])[0]
        if ei < 0:
            continue
        for name, kw in VARIANTS.items():
            for mode in ("intraday", "close"):
                ret, days = run(df, ei, mode, atr_pct=s.get("atr_pct"), **kw)
                rows.append({"var": name, "mode": mode, "year": s["year"], "ret": ret, "days": days})
    res = pd.DataFrame(rows)
    out = {mode: {name: _summ(g) for name, g in res[res["mode"] == mode].groupby("var", sort=False)}
           for mode in ("intraday", "close")}
    meta = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "market": market,
            "signals": int(len(ev)), "note": "signals passing screener/rules.py; no fees; same price data as the backtest"}
    (OUT / f"variants_{market}.json").write_text(json.dumps({**meta, "results": out}, indent=1))
    years = sorted(res["year"].unique())
    lines = [f"# Exit-rule variants {market.upper()}", "", f"- {meta['note']}", f"- signals: {len(ev)}", ""]
    for mode, d in out.items():
        lines += [f"## {mode} stop", "",
                  "| variant | win rate | not losing (>-1%) | avg win | avg loss | expectancy | PF | days | " + " | ".join(years) + " |",
                  "|---" * (8 + len(years)) + "|"]
        for name, x in d.items():
            yr = " | ".join(f"{x['by_year'].get(y, float('nan')):.1%}" for y in years)
            lines.append(f"| {name} | {x['win_rate']:.0%} | {x['not_losing_-1%']:.0%} | {x['avg_win']:.1%} | {x['avg_loss']:.1%} | "
                         f"{x['expectancy']:.2%} | {x['profit_factor']} | {x['days_median']:.0f} | {yr} |")
        lines.append("")
    (OUT / f"variants_{market}.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    sys.exit(main(p.parse_args().market))

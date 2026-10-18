"""Compare exit and add-on variants on the backtest signals that pass the market rules.

Reads data/eval/backtest_events_<market>.csv (written by screener.backtest), downloads the same
price history and replays each signal with different stop widths, break-even levels, trailing
stops, profit targets and add-on (pyramiding) rules. Writes data/eval/variants_<market>.{md,json}.

Returns are measured on the initial position (P&L of all lots / initial entry notional), so an
add-on that earns money raises the number and one that loses lowers it.

Usage: python -m screener.variants --market jp
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import indicators as ind

OUT = Path("data/eval")

CUR = "current: stop -8%, BE at +8%, 1/3 at +16%"
VARIANTS: dict[str, dict[str, dict]] = {
    "stop width": {
        CUR: {},
        "stop -6%": {"stop": 0.06},
        "stop -10%": {"stop": 0.10},
        "stop -12%": {"stop": 0.12},
        "stop 3x ATR (6-12%)": {"atr_mult": 3.0},
    },
    "break-even level (after a close >= +8%)": {
        **{f"BE +{int(x * 100)}%": {"be_level": x} for x in (0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06)},
        "BE +3% after +10%": {"be_at": 0.10, "be_level": 0.03},
        "BE +5% after +10%": {"be_at": 0.10, "be_level": 0.05},
        "BE +4% after +12%": {"be_at": 0.12, "be_level": 0.04},
        "BE +6% after +12%": {"be_at": 0.12, "be_level": 0.06},
    },
    "trailing stop from the high (after a close >= +8%)": {
        **{f"high -{int(x * 100)}%": {"hi_trail": x} for x in (0.05, 0.07, 0.10, 0.15)},
        "high -5%, no 1/3 trim": {"hi_trail": 0.05, "trim_at": None},
        "high -10%, no 1/3 trim": {"hi_trail": 0.10, "trim_at": None},
    },
    "profit taking": {
        "half at +8%, rest as current": {"trim_at": 0.08, "trim_frac": 0.5},
        "all out at +10%": {"full_at": 0.10},
        "no 1/3 trim (trail only)": {"trim_at": None},
    },
    "add-on (one add, before the +16% trim unless noted)": {
        "skill rule: +8% and new 3-month high, add 0.5x": {"add": "skill", "add_frac": 0.5},
        "skill rule, add 1x": {"add": "skill", "add_frac": 1.0},
        "re-break: pullback >=5% from the high, then close above it, add 0.5x": {"add": "rebreak", "add_pb": 0.05, "add_frac": 0.5},
        "re-break: pullback >=8%, add 0.5x": {"add": "rebreak", "add_pb": 0.08, "add_frac": 0.5},
        "re-break: pullback >=8%, add 1x": {"add": "rebreak", "add_pb": 0.08, "add_frac": 1.0},
        "re-break >=8%, add 0.5x, also after the trim": {"add": "rebreak", "add_pb": 0.08, "add_frac": 0.5, "add_after_trim": True},
    },
    "combined candidates": {
        "BE +1%, current ladder, skill add 0.5x": {"be_level": 0.01, "add": "skill", "add_frac": 0.5},
        "BE +1%, high -10%, no trim": {"be_level": 0.01, "hi_trail": 0.10, "trim_at": None},
        "BE +1%, high -10%, no trim, skill add 0.5x": {"be_level": 0.01, "hi_trail": 0.10, "trim_at": None,
                                                        "add": "skill", "add_frac": 0.5, "add_after_trim": True},
        "BE +1%, high -10%, no trim, skill add 1x": {"be_level": 0.01, "hi_trail": 0.10, "trim_at": None,
                                                      "add": "skill", "add_frac": 1.0, "add_after_trim": True},
        "BE +1%, high -12%, no trim, skill add 0.5x": {"be_level": 0.01, "hi_trail": 0.12, "trim_at": None,
                                                        "add": "skill", "add_frac": 0.5, "add_after_trim": True},
    },
}


def run(df: pd.DataFrame, ei: int, mode: str = "intraday", stop: float = 0.08, be_at: float = 0.08,
        be_level: float = 0.0, trim_at: float | None = 0.16, trim_frac: float = 1 / 3, full_at: float | None = None,
        trail: float = 0.15, hi_trail: float | None = None, max_hold: int = 120,
        atr_mult: float | None = None, atr_pct: float | None = None, atr_bounds: tuple[float, float] = (0.06, 0.12),
        add: str | None = None, add_frac: float = 0.5, add_pb: float = 0.08, add_after_trim: bool = False) -> dict:
    """The exit ladder of simulate.exit_rules with every level as a parameter, plus one optional add-on.

    Returns ret (P&L / initial notional), days, added (bool) and add_ret (P&L of the add lot / initial notional).
    """
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    sma50 = df["Close"].rolling(50).mean().to_numpy(float)
    hi63 = df["High"].rolling(ind.LOOKBACK_3M).max().shift(1).to_numpy(float)
    n, e = len(df), o[ei]
    if atr_mult is not None and atr_pct is not None and not math.isnan(atr_pct):
        stop = min(max(atr_mult * atr_pct, atr_bounds[0]), atr_bounds[1])
    sl = e * (1 - stop)
    qty, cost = 1.0, e            # position in units of the initial lot, average cost
    pnl = 0.0                     # realized P&L in price units per initial lot
    add_qty, add_px, add_pnl = 0.0, None, 0.0
    stage, trim_q, sell, add_pending, added = 0, 0.0, False, False, False
    hc, hh = e, e                 # highest close / high since entry
    peak, pulled = e, False       # for the re-break add
    last = min(n, ei + max_hold)

    def close_all(px):
        nonlocal pnl, add_pnl
        pnl += qty * (px - cost)
        if add_qty:
            add_pnl += add_qty * (px - add_px)

    def out(days):
        return {"ret": pnl / e, "days": int(days), "added": added, "add_ret": add_pnl / e}

    for j in range(ei, last):
        # orders at today's open
        if sell:
            close_all(o[j])
            return out(j - ei)
        if trim_q:
            q = min(trim_q, qty)
            pnl += q * (o[j] - cost)
            if add_qty:  # the add lot shares the trim pro rata
                aq = add_qty * q / qty
                add_pnl += aq * (o[j] - add_px)
                add_qty -= aq
            qty -= q
            trim_q = 0.0
            if qty <= 1e-9:
                return out(j - ei)
        if add_pending:
            cost = (qty * cost + add_frac * o[j]) / (qty + add_frac)
            qty += add_frac
            add_qty, add_px, added, add_pending = add_frac, o[j], True, False
        # stop during the session (intraday) or on the close
        if mode == "intraday":
            if o[j] <= sl or l[j] <= sl:
                close_all(min(o[j], sl))
                return out(j - ei)
        elif c[j] < sl:
            sell = True
            continue
        # end-of-day updates
        m50 = 0 if math.isnan(sma50[j]) else sma50[j]
        prev_peak = peak
        hc, hh = max(hc, c[j]), max(hh, h[j])
        if full_at is not None and c[j] >= e * (1 + full_at):
            trim_q = qty
            continue
        if stage < 1 and c[j] >= e * (1 + be_at):
            sl = max(sl, e * (1 + be_level))
            stage = 1
        if hi_trail is not None and stage >= 1:
            sl = max(sl, hh * (1 - hi_trail))
        if trim_at is not None and stage < 2 and c[j] >= e * (1 + trim_at):
            trim_q = qty * trim_frac
            stage = 2
            sl = max(sl, e * (1 + trim_at / 2), m50)
        elif stage >= 2 and (j - ei) % 5 == 0:
            sl = max(sl, hc * (1 - trail), m50)
        elif trim_at is None and stage >= 1 and hi_trail is None and (j - ei) % 5 == 0:
            sl = max(sl, hc * (1 - trail), m50)
        # add-on signal (bought at the next open); needs the stop at or above the entry
        if add and not added and not add_pending and stage >= 1 and (add_after_trim or stage < 2) and sl >= e:
            if add == "skill":
                ok = c[j] >= e * 1.08 and not math.isnan(hi63[j]) and c[j] > hi63[j]
            else:
                ok = pulled and prev_peak >= e * (1 + be_at) and c[j] > prev_peak
            if ok:
                add_pending = True
        if c[j] > peak:
            peak, pulled = c[j], False
        elif c[j] <= peak * (1 - add_pb):
            pulled = True
    j = last - 1
    close_all(c[j])
    return out(j - ei + 1)


def _summ(g: pd.DataFrame, stop: float = 0.08) -> dict:
    r = g["ret"]
    w, l = r[r > 0], r[r <= 0]
    yearly = g.groupby("year")["ret"].mean()
    res = {"n": int(len(r)), "win_rate": round(float((r > 0).mean()), 3),
           "avg_win": round(float(w.mean()), 4) if len(w) else None,
           "avg_loss": round(float(l.mean()), 4) if len(l) else None,
           "expectancy": round(float(r.mean()), 4),
           "profit_factor": round(float(w.sum() / -l.sum()), 2) if l.sum() < 0 else None,
           "days_median": float(g["days"].median()),
           "by_year": {str(k): round(float(v), 4) for k, v in yearly.items()}}
    if g["added"].any():
        a = g[g["added"]]
        res["added_share"] = round(float(g["added"].mean()), 3)
        res["add_lot_mean"] = round(float(a["add_ret"].mean()), 4)
        res["add_lot_win"] = round(float((a["add_ret"] > 0).mean()), 3)
    return res


def main(market: str) -> int:
    from .fetch import download  # needs yfinance; imported here so run() is testable without it

    ev = pd.read_csv(OUT / f"backtest_events_{market}.csv")
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
        for grp, vs in VARIANTS.items():
            for name, kw in vs.items():
                for mode in ("intraday", "close"):
                    r = run(df, ei, mode, atr_pct=s.get("atr_pct"), **kw)
                    rows.append({"grp": grp, "var": name, "mode": mode, "year": s["year"], **r})
    res = pd.DataFrame(rows)
    out: dict = {}
    for mode in ("intraday", "close"):
        out[mode] = {}
        for grp, vs in VARIANTS.items():
            sub = res[(res["mode"] == mode) & (res["grp"] == grp)]
            out[mode][grp] = {name: _summ(sub[sub["var"] == name]) for name in vs}
    meta = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "market": market,
            "signals": int(len(ev)), "note": "signals passing screener/rules.py; no fees; returns on the initial position"}
    (OUT / f"variants_{market}.json").write_text(json.dumps({**meta, "results": out}, indent=1))
    years = sorted(res["year"].unique())
    lines = [f"# Exit and add-on variants {market.upper()}", "", f"- {meta['note']}", f"- signals: {len(ev)}", ""]
    for mode, groups in out.items():
        lines.append(f"## {mode} stop")
        for grp, d in groups.items():
            lines += ["", f"### {grp}", "",
                      "| variant | win rate | avg win | avg loss | expectancy | PF | days | added | add lot mean | " + " | ".join(years) + " |",
                      "|---" * (9 + len(years)) + "|"]
            for name, x in d.items():
                yr = " | ".join(f"{x['by_year'].get(y, float('nan')):.1%}" for y in years)
                ad = f"{x['added_share']:.0%}" if "added_share" in x else "-"
                al = f"{x['add_lot_mean']:.2%}" if "add_lot_mean" in x else "-"
                lines.append(f"| {name} | {x['win_rate']:.0%} | {x['avg_win']:.1%} | {x['avg_loss']:.1%} | "
                             f"{x['expectancy']:.2%} | {x['profit_factor']} | {x['days_median']:.0f} | {ad} | {al} | {yr} |")
        lines.append("")
    (OUT / f"variants_{market}.md").write_text("\n".join(lines))
    res.drop(columns=["grp"]).groupby(["mode", "var"])["ret"].describe().to_csv(OUT / f"variants_dist_{market}.csv")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    sys.exit(main(p.parse_args().market))

"""Compare exit and add-on variants on the backtest signals that pass the market rules.

Reads data/eval/backtest_events_<market>.csv (written by screener.backtest), downloads the same
price history and replays each signal with the current rules (simulate.RULES), the previous rules
(simulate.OLD_RULES) and variations of the current ones. Writes data/eval/variants_<market>.{md,json}.

Returns are on the initial position (P&L of all lots / initial entry notional).

Usage: python -m screener.variants --market jp
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd

from . import indicators as ind
from .simulate import OLD_RULES, RULES, exit_rules

OUT = Path("data/eval")

CUR = "current: BE +1% at +8%, high -10%, add 0.5x"


def _v(**kw) -> dict:
    return {**RULES, **kw}


VARIANTS: dict[str, dict[str, dict]] = {
    "current vs previous": {
        CUR: _v(),
        "previous (until 2026-10-18): BE 0%, 1/3 at +16%, 15% trail": dict(OLD_RULES),
        "current without the add-on": _v(add=None),
    },
    "stop width": {f"stop -{int(x * 100)}%": _v(stop=x) for x in (0.06, 0.10, 0.12)},
    "break-even": {
        "BE +0%": _v(be_level=0.0),
        "BE +2%": _v(be_level=0.02),
        "BE +3% after +10%": _v(be_at=0.10, be_level=0.03),
    },
    "trailing stop from the high": {f"high -{int(x * 100)}%": _v(hi_trail=x) for x in (0.07, 0.08, 0.12, 0.15)},
    "add-on": {
        "add 1x": _v(add_frac=1.0),
        "add 0.33x": _v(add_frac=1 / 3),
        "add on re-break (pullback >= 5%)": _v(add="rebreak", add_pb=0.05),
    },
    "profit taking": {
        "1/3 at +16% as well": _v(trim_at=0.16),
        "1/3 at +30%": _v(trim_at=0.30),
    },
}


def run(df: pd.DataFrame, ei: int, mode: str = "intraday", **kw) -> dict:
    return exit_rules(df, ei, mode, **kw)


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

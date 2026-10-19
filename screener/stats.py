"""Summaries of followed signals: how often they work, how much, how fast, and how they fail."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .simulate import HORIZONS

MIN_GROUP = 20  # groups smaller than this are reported but marked as too small to act on


def _f(x, nd=4):
    return None if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))) else round(float(x), nd)


def summarize(ev: pd.DataFrame) -> dict:
    """ev: one row per signal with the columns produced by simulate.follow()."""
    out: dict = {"n": int(len(ev)), "enough": bool(len(ev) >= MIN_GROUP)}
    if ev.empty:
        return out
    for k in HORIZONS:
        s = ev[f"r{k}"].dropna()
        if len(s):
            out[f"r{k}"] = {"n": int(len(s)), "mean": _f(s.mean()), "median": _f(s.median()),
                            "pct_up": _f((s > 0).mean()), "p10": _f(s.quantile(0.1)), "p90": _f(s.quantile(0.9))}
    out["mfe60_median"] = _f(ev["mfe60"].median())
    out["mae60_median"] = _f(ev["mae60"].median())
    out["mae60_p10"] = _f(ev["mae60"].quantile(0.1))
    fh = ev["first_hit"].value_counts(dropna=False)
    out["first_hit"] = {"stop_-8%": int(fh.get("stop", 0)), "target_+16%": int(fh.get("target", 0)),
                        "neither_60d": int(len(ev) - fh.get("stop", 0) - fh.get("target", 0))}
    for mode in ("intraday", "close"):
        r = ev[f"{mode}_ret"].dropna()
        closed = ev[ev[f"{mode}_exit"] != "open"]
        win, loss = r[r > 0], r[r <= 0]
        out[f"rules_{mode}"] = {
            "n": int(len(r)), "still_open": int((ev[f"{mode}_exit"] == "open").sum()),
            "win_rate": _f((r > 0).mean()), "avg_win": _f(win.mean()), "avg_loss": _f(loss.mean()),
            "expectancy": _f(r.mean()), "median": _f(r.median()),
            "profit_factor": _f(win.sum() / -loss.sum()) if loss.sum() < 0 else None,
            "best": _f(r.max()), "worst": _f(r.min()),
            "days_median": _f(closed[f"{mode}_days"].median(), 1),
            "days_win_median": _f(closed.loc[closed[f"{mode}_ret"] > 0, f"{mode}_days"].median(), 1),
            "days_loss_median": _f(closed.loc[closed[f"{mode}_ret"] <= 0, f"{mode}_days"].median(), 1),
            "exits": {k: int(v) for k, v in ev[f"{mode}_exit"].value_counts().items()},
            "share_of_profit_top10pct": _f(r.nlargest(max(1, len(r) // 10)).sum() / r[r > 0].sum()) if (r > 0).any() else None,
        }
        if f"{mode}_added" in ev:
            ad = ev[f"{mode}_added"].fillna(False).astype(bool)
            out[f"rules_{mode}"]["added_share"] = _f(ad.mean())
            out[f"rules_{mode}"]["add_lot_mean"] = _f(ev.loc[ad, f"{mode}_add_ret"].mean()) if ad.any() else None
    return out


def _bucket_rs(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "unknown"
    return "90-99" if x >= 90 else ("80-89" if x >= 80 else ("70-79" if x >= 70 else "<70"))


def breakdown(ev: pd.DataFrame) -> dict:
    """Overall summary plus splits by signal, regime and each flag."""
    res = {"all": summarize(ev)}
    if ev.empty:
        return res
    key = "intraday_ret"
    res["by_year"] = {str(y): summarize(g) for y, g in ev.groupby(ev["signal_date"].str[:4])}
    if "rs_rating" in ev:
        res["by_rs_rating"] = {b: summarize(g) for b, g in ev.groupby(ev["rs_rating"].map(_bucket_rs))}
    if "regime_state" in ev:
        res["by_regime"] = {str(b): summarize(g) for b, g in ev.groupby(ev["regime_state"].fillna("unknown"))}
    if "dist_days" in ev:
        res["by_distribution_days"] = {b: summarize(g) for b, g in
                                       ev.groupby(np.where(ev["dist_days"].fillna(0) >= 5, ">=5", "<5"))}
    for col, name, bins, labels in (
            ("bench_gap", "by_benchmark_gap_at_entry", [-1, -0.02, -0.01, 0.01, 0.02, 1],
             ["<=-2%", "-2..-1%", "-1..+1%", "+1..+2%", ">=+2%"]),
            ("stock_gap", "by_stock_gap_at_entry", [-1, -0.02, 0, 0.02, 0.04, 1],
             ["<=-2%", "-2..0%", "0..+2%", "+2..+4%", ">=+4%"]),
            ("breadth50", "by_breadth50", [0, 0.45, 0.6, 0.75, 1.01], ["<45%", "45-60%", "60-75%", ">=75%"])):
        if col in ev and ev[col].notna().any():
            cut = pd.cut(ev[col], bins, labels=labels, right=False)
            res[name] = {str(b): summarize(g) for b, g in ev.groupby(cut, observed=True)}
    sig = {}
    for col in ("flags", "plus"):
        if col not in ev:
            continue
        names = sorted({f for fl in ev[col] for f in (fl or [])})
        for name in names:
            has = ev[col].map(lambda fl: name in (fl or []))
            a, b = ev[has], ev[~has]
            sig[f"{col}:{name}"] = {
                "with": _short(a, key), "without": _short(b, key),
                "diff_expectancy": _f(a[key].mean() - b[key].mean()) if len(a) and len(b) else None,
                "diff_r20": _f(a["r20"].mean() - b["r20"].mean()) if len(a) and len(b) else None,
            }
    res["by_signal"] = sig
    return res


def _short(g: pd.DataFrame, key: str) -> dict:
    r = g[key].dropna()
    return {"n": int(len(r)), "enough": bool(len(r) >= MIN_GROUP), "win_rate": _f((r > 0).mean()) if len(r) else None,
            "expectancy": _f(r.mean()) if len(r) else None, "r20_mean": _f(g["r20"].mean()) if len(g) else None,
            "stop_first": _f((g["first_hit"] == "stop").mean()) if len(g) else None}


def markdown(title: str, res: dict, notes: list[str]) -> str:
    """Compact human/LLM-readable report."""
    a = res["all"]
    lines = [f"# {title}", ""] + [f"- {x}" for x in notes] + [""]
    if not a.get("n"):
        return "\n".join(lines + ["No signals."])
    lines.append(f"Signals: {a['n']}")
    lines.append("")
    lines.append("| horizon | n | mean | median | % up | p10 | p90 |")
    lines.append("|---|---|---|---|---|---|---|")
    for k in HORIZONS:
        x = a.get(f"r{k}")
        if x:
            lines.append(f"| {k}d | {x['n']} | {x['mean']:.1%} | {x['median']:.1%} | {x['pct_up']:.0%} | {x['p10']:.1%} | {x['p90']:.1%} |")
    lines.append("")
    fh = a["first_hit"]
    lines.append(f"First within 60 sessions: -8% stop {fh['stop_-8%']}, +16% {fh['target_+16%']}, neither {fh['neither_60d']}. "
                 f"Median MFE {a['mfe60_median']:.1%}, median MAE {a['mae60_median']:.1%}, MAE p10 {a['mae60_p10']:.1%}.")
    lines.append("")
    lines.append("| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for mode in ("intraday", "close"):
        x = a[f"rules_{mode}"]
        pf = f"{x['profit_factor']:.2f}" if x["profit_factor"] is not None else "-"
        aw = f"{x['avg_win']:.1%}" if x["avg_win"] is not None else "-"
        al = f"{x['avg_loss']:.1%}" if x["avg_loss"] is not None else "-"
        top = f"{x['share_of_profit_top10pct']:.0%}" if x["share_of_profit_top10pct"] is not None else "-"
        lines.append(f"| {mode} stop | {x['n']} | {x['win_rate']:.0%} | {aw} | {al} | {x['expectancy']:.2%} | {pf} | "
                     f"{x['days_win_median']}/{x['days_loss_median']} | {top} |")
    adds = [f"{m}: added in {a[f'rules_{m}']['added_share']:.0%}, add lot mean {a[f'rules_{m}']['add_lot_mean']:.2%} of the initial position"
            for m in ("intraday", "close") if a[f"rules_{m}"].get("add_lot_mean") is not None]
    if adds:
        lines += ["", "Add-on: " + "; ".join(adds) + "."]
    for name in ("by_year", "by_regime", "by_distribution_days", "by_rs_rating", "by_benchmark_gap_at_entry",
                 "by_stock_gap_at_entry", "by_breadth50"):
        if name in res:
            lines += ["", f"## {name}", "", "| group | n | win rate | expectancy | 20d mean |", "|---|---|---|---|---|"]
            for g, x in res[name].items():
                ri = x.get("rules_intraday", {})
                r20 = x.get("r20", {}).get("mean")
                lines.append(f"| {g} | {x['n']}{'' if x['enough'] else ' (small)'} | "
                             f"{ri.get('win_rate') if ri.get('win_rate') is None else format(ri['win_rate'], '.0%')} | "
                             f"{ri.get('expectancy') if ri.get('expectancy') is None else format(ri['expectancy'], '.2%')} | "
                             f"{r20 if r20 is None else format(r20, '.1%')} |")
    if res.get("by_signal"):
        lines += ["", "## signals (intraday-stop expectancy, with vs without)", "",
                  "| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |", "|---|---|---|---|---|---|---|"]
        items = sorted(res["by_signal"].items(), key=lambda kv: -(kv[1]["with"]["n"]))
        for k, v in items:
            w, wo = v["with"], v["without"]
            fmt = lambda x, f: "-" if x is None else format(x, f)  # noqa: E731
            lines.append(f"| {k} | {w['n']}{'' if w['enough'] else ' (small)'} | {fmt(w['win_rate'], '.0%')} | "
                         f"{fmt(w['expectancy'], '.2%')} | {fmt(wo['expectancy'], '.2%')} | {fmt(v['diff_expectancy'], '+.2%')} | "
                         f"{fmt(w['stop_first'], '.0%')} |")
    return "\n".join(lines) + "\n"


TRIGGER_NAMES = {"a_breakout": "(a) breakout with volume, next open",
                 "b_near_high": "(b) within 3% of the 3-month high, next open",
                 "b_near_high_stop": "(b) same, buy-stop above the high within 5 sessions",
                 "c_pullback": "(c) pullback re-entry, next open"}


def trigger_table(trig: dict, by_year: dict) -> str:
    """Comparison of entry types (signals passing the market rules)."""
    if not trig:
        return ""
    years = sorted({y for d in by_year.values() for y in d})
    lines = ["## Entry types (signals passing the market rules)", "",
             "| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: " + " / ".join(years) + " |",
             "|---|---|---|---|---|---|---|"]
    for k, x in trig.items():
        if not x.get("n"):
            continue
        ri, rc = x["rules_intraday"], x["rules_close"]
        yr = " / ".join(f"{by_year[k][y]['rules_close']['expectancy']:.1%}" if y in by_year[k] and by_year[k][y].get("n") else "-" for y in years)
        r20 = x.get("r20", {}).get("mean")
        lines.append(f"| {TRIGGER_NAMES.get(k, k)} | {x['n']} | {ri['win_rate']:.0%} / {rc['win_rate']:.0%} | {ri['expectancy']:.2%} | "
                     f"{rc['expectancy']:.2%} | {'-' if r20 is None else format(r20, '.1%')} | {yr} |")
    return "\n".join(lines) + "\n"

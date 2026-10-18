"""Follow every live candidate (A and B lists in data/history) forward, whether or not it was bought.

Entry is the next session's open after the list date. Outputs data/eval/live_<market>.{json,md}
and the per-signal table live_events_<market>.csv.

Usage: python -m screener.evaluate --market jp
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import pandas as pd

from . import indicators as ind
from . import simulate, stats
from .fetch import download

HIST = Path("data/history")
OUT = Path("data/eval")


def log(*a):
    print(dt.datetime.now().strftime("%H:%M:%S"), *a, file=sys.stderr, flush=True)


def load_signals(market: str) -> pd.DataFrame:
    rows = []
    for f in sorted(HIST.glob(f"*_{market}.json")):
        d = json.loads(f.read_text())
        for rank in ("A", "B"):
            for r in d.get(rank, []):
                rows.append({"ticker": r["ticker"], "signal_date": r.get("date") or f.name[:10], "rank": rank,
                             "rs_rating": r.get("rs_rating"), "triggers": r.get("triggers") or [],
                             "flags": [x for x in (r.get("flags") or []) if x != "fin_unknown"],
                             "plus": r.get("plus") or [], "close": r.get("close")})
    ev = pd.DataFrame(rows)
    if ev.empty:
        return ev
    # one row per ticker and signal date (A wins over B)
    return ev.sort_values("rank").drop_duplicates(["ticker", "signal_date"]).reset_index(drop=True)


def main(market: str) -> int:
    sig = load_signals(market)
    OUT.mkdir(parents=True, exist_ok=True)
    if sig.empty:
        log("no signals yet")
        return 0
    first = pd.Timestamp(sig["signal_date"].min())
    days = (pd.Timestamp.now() - first).days + 30
    period = "1y" if days < 330 else ("2y" if days < 700 else "5y")
    prices = download(sorted(sig["ticker"].unique()), period=period, auto_adjust=False, intraday=False)
    rows = []
    for _, s in sig.iterrows():
        df = prices.get(s["ticker"])
        if df is None or df.empty:
            continue
        df = ind._clean(df)
        later = df.index > pd.Timestamp(s["signal_date"])
        if not later.any():
            continue  # no session after the signal yet
        entry_i = int(later.argmax())
        rows.append({**s.to_dict(), **simulate.follow(df, entry_i)})
    ev = pd.DataFrame(rows)
    log(f"followed: {len(ev)} of {len(sig)}")
    res = {"A": stats.breakdown(ev[ev["rank"] == "A"]) if len(ev) else {},
           "B": stats.summarize(ev[ev["rank"] == "B"]) if len(ev) else {}}
    notes = [f"market: {market}, live lists from {sig['signal_date'].min()} to {sig['signal_date'].max()}",
             "every A and B name is followed whether or not it was bought; entry at the next open after the list date",
             "young signals have only a few sessions; horizons without data are left out"]
    meta = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "market": market,
            "signals": int(len(ev)), "notes": notes}
    (OUT / f"live_{market}.json").write_text(json.dumps({**meta, "results": res}, ensure_ascii=False, indent=1, default=str))
    md = stats.markdown(f"Live A-candidates {market.upper()}", res["A"], notes) if res["A"] else "# no A signals\n"
    if res["B"].get("n"):
        b = res["B"]
        ri = b.get("rules_intraday", {})
        md += (f"\n## B-candidates (no trigger yet)\n\nn={b['n']}, 20d mean "
               f"{b.get('r20', {}).get('mean')}, rules expectancy {ri.get('expectancy')}\n")
    (OUT / f"live_{market}.md").write_text(md)
    if len(ev):
        ev.to_csv(OUT / f"live_events_{market}.csv", index=False)
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    sys.exit(main(p.parse_args().market))

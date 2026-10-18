"""Compact price table for every priced ticker (screening universe + extras.txt) -> data/prices_<market>.json.

Generic market data only: nothing here identifies anyone's holdings.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def extras(market: str) -> list[str]:
    ts = [l.strip() for l in (ROOT / "extras.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]
    jp = [t for t in ts if t.endswith(".T") or t in ("^N225", "JPY=X", "EURJPY=X")]
    return jp if market == "jp" else [t for t in ts if t not in jp] + ["JPY=X"]


def _rsi(c: pd.Series, n: int = 14):
    d = c.diff().dropna()
    if len(d) < n:
        return None
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean().iloc[-1]
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean().iloc[-1]
    return 100.0 if dn == 0 else float(100 - 100 / (1 + up / dn))


def _r(x, nd=4):
    if x is None:
        return None
    x = float(x)
    return None if math.isnan(x) or math.isinf(x) else round(x, nd)


def row(df: pd.DataFrame) -> dict | None:
    source = df.attrs.get("close_source")
    df = df.dropna(subset=["Close"])
    if df.empty:
        return None
    c = df["Close"]
    return {
        "d": str(df.index[-1].date()),
        "c": _r(c.iloc[-1]), "pc": _r(c.iloc[-2]) if len(c) > 1 else None,
        "h": _r(df["High"].iloc[-1]), "l": _r(df["Low"].iloc[-1]), "v": _r(df["Volume"].iloc[-1], 0),
        "s20": _r(c.rolling(20).mean().iloc[-1]), "s50": _r(c.rolling(50).mean().iloc[-1]),
        "s200": _r(c.rolling(200).mean().iloc[-1]),
        "h3m": _r(df["High"].iloc[-63:].max()), "h52": _r(df["High"].iloc[-252:].max()),
        "rsi": _r(_rsi(c), 1), "r6m": _r(c.iloc[-1] / c.iloc[-127] - 1) if len(c) > 127 else None,
        # last 60 closes, oldest first (ends at "d") — for "highest close since entry"
        "c60": [_r(x) for x in c.iloc[-60:].tolist()],
        # last 60 session highs, oldest first — for the trailing stop "highest high since entry -10%"
        "h60": [_r(x) for x in df["High"].iloc[-60:].tolist()],
        # source of the latest close: "official" (Yahoo quote), "60m" (rebuilt from hourly bars) or "d" (daily bar)
        "cs": {"official": "o", "60m": "h"}.get(source, "d"),
    }


def write(market: str, prices: dict[str, pd.DataFrame], names: dict[str, str]) -> int:
    out = {}
    for t, df in prices.items():
        try:
            rw = row(df)
        except Exception:  # noqa: BLE001
            rw = None
        if rw:
            if names.get(t):
                rw["n"] = names[t]
            out[t] = rw
    res = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "market": market,
        "keys": "d=date c=close pc=prev close h/l=high/low v=volume s20/s50/s200=SMA h3m/h52=3m/52w high "
                "rsi=RSI14 r6m=6m return c60/h60=last 60 closes/highs oldest first n=name cs=close source (d daily bar, o official quote, h hourly rebuild)",
        "note": "Actual (unadjusted) prices. The latest JP session may be rebuilt from 60m bars, so its close can differ slightly from the official close.",
        "prices": out,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / f"prices_{market}.json").write_text(json.dumps(res, ensure_ascii=False, separators=(",", ":")),
                                                         encoding="utf-8")
    return len(out)

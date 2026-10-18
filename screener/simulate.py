"""Follow a signal forward: fixed-horizon returns, excursions and the exit-rule simulation.

The exit rules mirror the ones the screener's README describes for momentum trades:
- stop at -8% of the entry;
- close >= +8%  -> stop raised to the entry;
- close >= +16% -> sell 1/3 at the next open, stop = max(+8%, 50-day SMA);
- after that, every 5 sessions the stop is raised to max(highest close * 0.85, 50-day SMA); it never goes down.

Two stop styles are simulated: "intraday" (a resting stop order fills at the stop, or at the open
if the open gaps below it) and "close" (the stop is checked on the close and the position is sold
at the next open, as with odd-lot orders that cannot rest as stops).
"""
from __future__ import annotations

import math

import pandas as pd

HORIZONS = (5, 10, 20, 40, 60)
MAX_HOLD = 120
STOP = 0.08
BREAKEVEN_AT = 0.08
TRIM_AT = 0.16
TRAIL = 0.15
TRAIL_EVERY = 5


def _r(x: float | None, nd: int = 4):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), nd)


def forward(df: pd.DataFrame, entry_i: int) -> dict:
    """Returns at fixed horizons and the max favourable/adverse excursion over 60 sessions."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    n = len(df)
    entry = o[entry_i]
    out = {"entry": _r(entry, 2), "entry_date": str(df.index[entry_i].date())}
    for k in HORIZONS:
        j = entry_i + k - 1
        out[f"r{k}"] = _r(c[j] / entry - 1) if j < n else None
    end = min(n, entry_i + 60)
    out["sessions_seen"] = end - entry_i
    out["mfe60"] = _r(h[entry_i:end].max() / entry - 1)
    out["mae60"] = _r(l[entry_i:end].min() / entry - 1)
    # which came first: -8% (intraday low) or +16% (close)
    first = None
    for j in range(entry_i, end):
        if l[j] <= entry * (1 - STOP):
            first = "stop"
            break
        if c[j] >= entry * (1 + TRIM_AT):
            first = "target"
            break
    out["first_hit"] = first
    return out


def exit_rules(df: pd.DataFrame, entry_i: int, mode: str = "intraday") -> dict:
    """Simulate the exit ladder. Returns the blended return of the position and how it ended."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    sma50 = df["Close"].rolling(50).mean().to_numpy(float)
    n = len(df)
    entry = o[entry_i]
    stop = entry * (1 - STOP)
    stage = 0
    remaining = 1.0
    realized = 0.0
    trim_pending = False
    sell_next_open = False
    high_close = entry
    last = min(n, entry_i + MAX_HOLD)
    for j in range(entry_i, last):
        # orders executed at today's open
        if sell_next_open:
            realized += remaining * (o[j] / entry - 1)
            return _done(realized, j - entry_i, "stop_close", stage)
        if trim_pending:
            realized += (1 / 3) * (o[j] / entry - 1)
            remaining -= 1 / 3
            trim_pending = False
        # resting stop order during the session
        if mode == "intraday":
            if o[j] <= stop:
                realized += remaining * (o[j] / entry - 1)
                return _done(realized, j - entry_i, "stop_gap", stage)
            if l[j] <= stop:
                realized += remaining * (stop / entry - 1)
                return _done(realized, j - entry_i, "stop", stage)
        elif c[j] < stop:
            sell_next_open = True
            continue
        # end-of-day updates
        high_close = max(high_close, c[j])
        if stage < 1 and c[j] >= entry * (1 + BREAKEVEN_AT):
            stop = max(stop, entry)
            stage = 1
        if stage < 2 and c[j] >= entry * (1 + TRIM_AT):
            trim_pending = True
            stage = 2
            stop = max(stop, entry * (1 + BREAKEVEN_AT), sma50[j] if not math.isnan(sma50[j]) else 0)
        elif stage >= 2 and (j - entry_i) % TRAIL_EVERY == 0:
            stop = max(stop, high_close * (1 - TRAIL), sma50[j] if not math.isnan(sma50[j]) else 0)
    j = last - 1
    realized += remaining * (c[j] / entry - 1)
    reason = "max_hold" if last - entry_i >= MAX_HOLD else "open"
    return _done(realized, j - entry_i + 1, reason, stage)


def _done(ret: float, days: int, reason: str, stage: int) -> dict:
    return {"ret": _r(ret), "days": int(days), "exit": reason, "stage": stage}


def follow(df: pd.DataFrame, entry_i: int) -> dict:
    out = forward(df, entry_i)
    for mode in ("intraday", "close"):
        r = exit_rules(df, entry_i, mode)
        out.update({f"{mode}_{k}": v for k, v in r.items()})
    return out

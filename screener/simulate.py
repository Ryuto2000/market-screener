"""Follow a signal forward: fixed-horizon returns, excursions and the exit-rule simulation.

Exit rules for momentum trades (from 2026-10-18, chosen with screener.variants):
- stop at -8% of the entry;
- close >= +8% -> stop raised to the entry +1%;
- from then on the stop is max(entry +1%, highest high since entry -10%), updated daily; it never goes down;
- no partial profit taking;
- one add-on of half the initial size at the next open when the close is >= +8% and above the prior
  3-month high (the stop is already at entry +1%);
- earnings (from 2026-10-19): sold at the close before the results unless the stop is already at entry +1%
  or higher (follow() with earn_days; the backtest estimates the dates from volume spikes, screener.earnings).

Two stop styles are simulated: "intraday" (a resting stop order fills at the stop, or at the open
if the open gaps below it) and "close" (the stop is checked on the close and the position is sold
at the next open, as with odd-lot orders that cannot rest as stops).

Returns are on the initial position: P&L of all lots / initial entry notional.
The previous rules (until 2026-10-18) are available as OLD_RULES for comparison.
"""
from __future__ import annotations

import math

import pandas as pd

HORIZONS = (5, 10, 20, 40, 60)
MAX_HOLD = 250        # about a year; the live rules have no time limit
STOP = 0.08
TARGET = 0.16         # only for the descriptive "first hit" statistic
LOOKBACK_3M = 63

RULES = dict(stop=0.08, be_at=0.08, be_level=0.01, hi_trail=0.10, trim_at=None,
             add="skill", add_frac=0.5, add_after_trim=True)
OLD_RULES = dict(stop=0.08, be_at=0.08, be_level=0.0, hi_trail=None, trim_at=0.16, trim_frac=1 / 3,
                 trail=0.15, add=None)


def _r(x: float | None, nd: int = 4):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), nd)


def forward(df: pd.DataFrame, entry_i: int, entry_px: float | None = None) -> dict:
    """Returns at fixed horizons and the max favourable/adverse excursion over 60 sessions.
    entry_px: fill price on session entry_i (default: its open), e.g. a buy-stop above the open."""
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    n = len(df)
    entry = entry_px if entry_px is not None else o[entry_i]
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
        if c[j] >= entry * (1 + TARGET):
            first = "target"
            break
    out["first_hit"] = first
    return out


def exit_rules(df: pd.DataFrame, ei: int, mode: str = "intraday", stop: float = 0.08, be_at: float = 0.08,
               be_level: float = 0.01, trim_at: float | None = None, trim_frac: float = 1 / 3,
               full_at: float | None = None, trail: float = 0.15, hi_trail: float | None = 0.10,
               max_hold: int = MAX_HOLD, atr_mult: float | None = None, atr_pct: float | None = None,
               atr_bounds: tuple[float, float] = (0.06, 0.12), add: str | None = "skill", add_frac: float = 0.5,
               add_pb: float = 0.08, add_after_trim: bool = True, entry_px: float | None = None,
               earn_days=None, earn_mode: str | None = None) -> dict:
    """Simulate the exit ladder (defaults = current rules) with every level as a parameter.

    Legacy ladder (OLD_RULES): trim_frac of the position at the next open after a close >= trim_at,
    stop then max(entry * (1 + trim_at / 2), 50-day SMA), and every 5 sessions max(highest close * (1 - trail), SMA50).
    add: None, "skill" (close >= +8% and above the prior 3-month high) or "rebreak" (a pullback of add_pb from the
    highest close, then a close above it). Both need the stop at or above the entry.

    earn_days: positions of earnings reaction sessions; earn_mode "always" sells at the close before each one,
    "unless_be" only while the stop is still below the entry (stage 0), None ignores earnings.

    Returns ret (P&L / initial notional), days, exit, stage (0 none, 1 stop at/above entry, 2 trimmed),
    added (bool) and add_ret (P&L of the add lot / initial notional).
    """
    o, h, l, c = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close"))
    sma50 = df["Close"].rolling(50).mean().to_numpy(float)
    hi63 = df["High"].rolling(LOOKBACK_3M).max().shift(1).to_numpy(float)
    n, e = len(df), (entry_px if entry_px is not None else o[ei])
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
    earn_set = set(int(x) for x in earn_days) if (earn_mode and earn_days is not None) else set()

    def close_all(px):
        nonlocal pnl, add_pnl
        pnl += qty * (px - cost)
        if add_qty:
            add_pnl += add_qty * (px - add_px)

    def out(days, reason):
        return {"ret": _r(pnl / e), "days": int(days), "exit": reason, "stage": stage,
                "added": added, "add_ret": _r(add_pnl / e)}

    for j in range(ei, last):
        # orders at today's open
        if sell:
            close_all(o[j])
            return out(j - ei, "stop_close")
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
                return out(j - ei, "target")
        if add_pending:
            cost = (qty * cost + add_frac * o[j]) / (qty + add_frac)
            qty += add_frac
            add_qty, add_px, added, add_pending = add_frac, o[j], True, False
        # stop during the session (intraday) or on the close
        if mode == "intraday":
            if o[j] <= sl:
                close_all(o[j])
                return out(j - ei, "stop_gap")
            if l[j] <= sl:
                close_all(sl)
                return out(j - ei, "stop")
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
                ok = c[j] >= e * (1 + be_at) and not math.isnan(hi63[j]) and c[j] > hi63[j]
            else:
                ok = pulled and prev_peak >= e * (1 + be_at) and c[j] > prev_peak
            if ok:
                add_pending = True
        if c[j] > peak:
            peak, pulled = c[j], False
        elif c[j] <= peak * (1 - add_pb):
            pulled = True
        # earnings tomorrow: sell at today's close (odd lots can be sold at the afternoon close)
        if earn_set and (j + 1) in earn_set and j > ei and (earn_mode == "always" or stage < 1):
            close_all(c[j])
            return out(j - ei, "earnings")
    j = last - 1
    close_all(c[j])
    return out(j - ei + 1, "max_hold" if last - ei >= max_hold else "open")


def follow(df: pd.DataFrame, entry_i: int, entry_px: float | None = None, earn_days=None) -> dict:
    """earn_days: (estimated) earnings reaction sessions; positions still below the +8% stage are sold at the
    close before them (rule from 2026-10-19 for odd lots and unit shares alike)."""
    out = forward(df, entry_i, entry_px)
    for mode in ("intraday", "close"):
        r = exit_rules(df, entry_i, mode, entry_px=entry_px, earn_days=earn_days,
                       earn_mode="unless_be" if earn_days is not None else None)
        out.update({f"{mode}_{k}": v for k, v in r.items()})
    return out

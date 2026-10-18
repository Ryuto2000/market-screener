"""Market-specific filters chosen from the backtest (data/eval). They decide A/B eligibility.

Japan (2022-09 to 2026-10, 4,401 breakout signals): high volatility (ATR > 4%, i.e. the -8% stop is
within 2 ATR), deep bases (> 35%), overheated names (RSI > 80 or > 40% above the 200-day SMA) and the
very top RS ratings (>= 95) all lowered the expectancy of the exit rules; RS ranking otherwise did not
help, so lower volatility ranks first. Power gaps were not supportive in Japan.

US (2,649 signals): the edge after ~1% round-trip fees only survived with RS rating >= 90, the
benchmark in an uptrend and fewer than 5 distribution days in 25 sessions.
"""
from __future__ import annotations

# Position risk: Japan risks 0.5% of assets per trade (instead of 0.3%) when >= 75% of liquid names close
# above their 50-day SMA. Backtest (S-kabu close stop, 2,598 signals): +11.1% per trade vs +4.2%, better in 4 of 5 years.
RISK_BASE = 0.003
RISK_STRONG = 0.005
JP_STRONG_BREADTH = 75.0

JP_EXCLUDE_FLAGS = {"stop_inside_noise", "deep_base", "overheat"}
JP_MAX_RS = 95
US_MIN_RS = 90
US_MAX_DIST_DAYS = 5


def check(market: str, rec: dict, regime: dict | None) -> tuple[bool, str]:
    """(passes, reason). rec carries flags and rs_rating; regime carries benchmark state and distribution days."""
    flags = set(rec.get("flags") or [])
    rs = rec.get("rs_rating")
    if market == "jp":
        hit = sorted(flags & JP_EXCLUDE_FLAGS)
        if hit:
            return False, "excluded: " + ", ".join(hit)
        if rs is not None and rs >= JP_MAX_RS:
            return False, f"excluded: rs_rating >= {JP_MAX_RS}"
        return True, ""
    if rs is None or rs < US_MIN_RS:
        return False, f"rs_rating < {US_MIN_RS}"
    if regime:
        if regime.get("benchmark_state") not in (None, "uptrend"):
            return False, "benchmark not in an uptrend"
        if (regime.get("benchmark_distribution_days_25") or 0) >= US_MAX_DIST_DAYS:
            return False, f"{US_MAX_DIST_DAYS}+ distribution days"
    return True, ""


def rank_key(market: str, rec: dict):
    """Higher sorts first."""
    breakout = "a_breakout" in (rec.get("triggers") or [])
    fin_known = "fin_unknown" not in (rec.get("flags") or [])
    if market == "jp":
        atr = rec.get("atr_pct")
        return (breakout, fin_known, -(atr if atr is not None else 1.0), rec.get("vol_ratio") or 0)
    return (breakout, fin_known, rec.get("rs_rating") or 0, len(rec.get("triggers") or []), rec.get("vol_ratio") or 0)


def tidy_signals(market: str, rec: dict) -> None:
    """Japan: a power gap is information, not a supportive signal."""
    if market == "jp" and "power_gap" in (rec.get("plus") or []):
        rec["plus"] = [p for p in rec["plus"] if p != "power_gap"]
        rec.setdefault("info", []).append("power_gap")


def risk_per_trade(market: str, regime: dict | None) -> float:
    """Share of total assets to risk on one new trade, from market breadth (pct_above_sma50, in %)."""
    b = (regime or {}).get("pct_above_sma50")
    if market == "jp" and b is not None and b >= JP_STRONG_BREADTH:
        return RISK_STRONG
    return RISK_BASE

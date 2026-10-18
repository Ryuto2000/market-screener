"""Daily momentum screener. Usage: python -m screener.run --market jp|us

Writes data/<market>.json (latest), data/history/<date>_<market>.json and data/prices_<market>.json.
"rank_hint" is a mechanical label; verify with live data before acting on anything.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from . import fetch
from . import indicators as ind
from . import prices as price_table
from . import rules
from .universe import jp_universe, us_universe

CFG = {
    "jp": {"bench": "1306.T", "bench_name": "TOPIX (1306)", "min_turnover": 3e8, "min_mcap": 1e10, "ccy": "JPY"},
    "us": {"bench": "SPY", "bench_name": "S&P 500 (SPY)", "min_turnover": 2e7, "min_mcap": 2e9, "ccy": "USD"},
}
CRYPTO_WORDS = ("coin", "crypto", "bitcoin", "blockchain", "metaplanet", "メタプラネット", "strategy inc",
                "marathon digital", "mara holdings", "riot platforms", "galaxy digital", "暗号", "ビットコイン")
CHUNK = 150
DETAIL_LIMIT = 250  # earnings/fundamentals lookups (2 requests each)
# Yahoo's quarterly statements for most Tokyo listings come back empty or fail ("Invalid Crumb"); skip them there.
FUNDAMENTALS = {"jp": False, "us": True}
DATA = Path(__file__).resolve().parent.parent / "data"


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def _retry(fn, tries=3, wait=5):
    for k in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            log(f"retry after error: {e}")
            time.sleep(wait * (k + 1))


def download(tickers: list[str]) -> dict[str, pd.DataFrame]:
    return fetch.download(tickers, chunk=CHUNK, auto_adjust=False)  # actual traded prices


def market_cap(t: yf.Ticker) -> float | None:
    try:
        v = t.fast_info.get("marketCap") if hasattr(t.fast_info, "get") else t.fast_info.market_cap
        return float(v) if v else None
    except Exception:  # noqa: BLE001
        return None


def next_earnings(t: yf.Ticker) -> str | None:
    try:
        cal = t.calendar
        dates = cal.get("Earnings Date") if isinstance(cal, dict) else None
        if dates:
            today = dt.date.today()
            fut = sorted(d for d in dates if d >= today)
            return str(fut[0]) if fut else None
    except Exception:  # noqa: BLE001
        pass
    return None


_FIN_ERRORS: list[str] = []


def yoy(t: yf.Ticker) -> tuple[float | None, float | None, str | None]:
    """YoY change of the latest quarter's revenue and operating income (retries on rate limits)."""
    q = None
    for k in range(3):
        try:
            q = t.quarterly_income_stmt
            break
        except Exception as e:  # noqa: BLE001
            if len(_FIN_ERRORS) < 5:
                _FIN_ERRORS.append(f"{t.ticker}: {type(e).__name__}: {str(e)[:120]}")
            time.sleep(3 * (k + 1))
    try:
        if q is None or q.empty:
            return None, None, None
        cols = sorted(q.columns, reverse=True)
        latest = cols[0]
        prev = next((c for c in cols[1:] if 330 <= (latest - c).days <= 400), None)
        if prev is None:
            return None, None, str(latest.date())

        def chg(row):
            if row not in q.index:
                return None
            a, b = q.at[row, latest], q.at[row, prev]
            if pd.isna(a) or pd.isna(b) or b == 0:
                return None
            return float(a / abs(b) - 1) if b > 0 else float((a - b) / abs(b))
        return chg("Total Revenue"), chg("Operating Income"), str(latest.date())
    except Exception as e:  # noqa: BLE001
        if len(_FIN_ERRORS) < 5:
            _FIN_ERRORS.append(f"{t.ticker}: parse {type(e).__name__}: {str(e)[:120]}")
        return None, None, None


def bdays_until(date_str: str | None) -> int | None:
    if not date_str:
        return None
    return int(np.busday_count(dt.date.today(), dt.date.fromisoformat(date_str)))


def clean(o):
    if isinstance(o, float):
        return None if math.isnan(o) or math.isinf(o) else round(o, 4)
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return clean(float(o))
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def main(market: str) -> int:
    cfg = CFG[market]
    started = dt.datetime.now(dt.timezone.utc)
    uni = jp_universe() if market == "jp" else us_universe()
    log(f"universe: {len(uni)}")

    bench_df = download([cfg["bench"]]).get(cfg["bench"])
    bench_ret = ind.benchmark_ret_6m(bench_df) if bench_df is not None else None
    if bench_df is not None and not bench_df.empty:
        log(f"benchmark last bars: {[str(d.date()) for d in bench_df.dropna(subset=['Close']).index[-3:]]}")
    extra = [t for t in price_table.extras(market) if t not in set(uni["ticker"])]
    prices_all = download(uni["ticker"].tolist() + extra)
    prices = {t: df for t, df in prices_all.items() if t not in extra}

    last_dates = pd.Series([str(df.dropna(subset=["Close"]).index[-1].date()) for df in prices.values()
                            if df is not None and not df.dropna(subset=["Close"]).empty]).value_counts()
    log(f"last bar dates: {last_dates.head(3).to_dict()}")
    errors, rows = [], []
    meta = uni.set_index("ticker").to_dict("index")
    for tk, df in prices.items():
        try:
            m = ind.compute(df, bench_ret)
        except Exception as e:  # noqa: BLE001
            errors.append({"ticker": tk, "error": str(e)[:200]})
            continue
        if not m.ok:
            continue
        if m.turnover_20d < cfg["min_turnover"]:
            continue
        rows.append((tk, m))
    missing = sorted(set(uni["ticker"]) - set(prices))
    errors += [{"ticker": t, "error": "no price data"} for t in missing[:300]]
    log(f"liquid & enough history: {len(rows)}")

    # RS rating: percentile (1-99) of the weighted return among liquid names
    raw = pd.Series({tk: m.rs_raw for tk, m in rows}).dropna()
    rs_rating = (raw.rank(pct=True) * 98 + 1).round().astype(int).to_dict() if len(raw) else {}

    # market regime: benchmark trend + breadth of liquid names
    def _pct(cond):
        return round(100 * sum(1 for _, m in rows if cond(m)) / len(rows), 1) if rows else None
    bclose = bench_df["Close"].dropna() if bench_df is not None else pd.Series(dtype=float)
    b50 = float(bclose.rolling(50).mean().iloc[-1]) if len(bclose) >= 50 else None
    b200 = float(bclose.rolling(200).mean().iloc[-1]) if len(bclose) >= 200 else None
    blast = float(bclose.iloc[-1]) if len(bclose) else None
    if blast and b50 and b200:
        state = "uptrend" if blast > b50 > b200 else ("downtrend" if blast < b200 and b50 < b200 else "mixed")
    else:
        state = None
    regime = {"benchmark_close": blast, "benchmark_sma50": b50, "benchmark_sma200": b200, "benchmark_state": state,
              "pct_above_sma50": _pct(lambda m: m.close > m.sma50), "pct_above_sma200": _pct(lambda m: m.close > m.sma200),
              "pct_trend_template": _pct(lambda m: m.trend_ok),
              "benchmark_distribution_days_25": ind.distribution_days(bench_df) if bench_df is not None else None}
    if (regime["benchmark_distribution_days_25"] or 0) >= 5:
        regime["caution"] = "5+ distribution days in 25 sessions"
    log(f"regime: {regime}")

    trend = [(tk, m) for tk, m in rows if m.trend_ok]
    trend.sort(key=lambda x: (bool(x[1].triggers), rs_rating.get(x[0], 0)), reverse=True)
    log(f"trend + RS pass: {len(trend)}")

    out = []
    for n_done, (tk, m) in enumerate(trend):
        t = yf.Ticker(tk)
        mcap = market_cap(t)
        rec = {"ticker": tk, **{k: meta.get(tk, {}).get(k) for k in ("code", "name", "market", "sector")}}
        rec.update(m.to_dict())
        rec["market_cap"] = mcap
        rec["liquidity_ok"] = bool(mcap is None or mcap >= cfg["min_mcap"])
        if mcap is None:
            rec["flags"].append("mcap_unknown")
        name = str(rec.get("name") or "").lower()
        if any(w in name for w in CRYPTO_WORDS):
            rec["flags"].append("crypto_related")
        last_turnover = float(prices[tk]["Close"].iloc[-1] * prices[tk]["Volume"].iloc[-1])
        if mcap and last_turnover > mcap:
            rec["flags"].append("turnover_gt_mcap")
        if n_done < DETAIL_LIMIT:
            rec["next_earnings"] = next_earnings(t)
            rec["bdays_to_earnings"] = bdays_until(rec["next_earnings"])
            if FUNDAMENTALS[market]:
                rec["rev_yoy"], rec["op_income_yoy"], rec["fin_quarter"] = yoy(t)
            else:
                rec["rev_yoy"] = rec["op_income_yoy"] = rec["fin_quarter"] = None
            time.sleep(0.3)
        else:
            rec["next_earnings"] = rec["bdays_to_earnings"] = None
            rec["rev_yoy"] = rec["op_income_yoy"] = rec["fin_quarter"] = None

        checks = {
            "liquidity": rec["liquidity_ok"],
            "not_excluded": not ({"crypto_related", "turnover_gt_mcap"} & set(rec["flags"])),
            "trigger": bool(m.triggers),
            "chase_ok": bool(m.chase_ok) if m.triggers else False,
            # unknown fundamentals do not fail the screen (flagged fin_unknown instead)
            "fundamentals": not ((rec["rev_yoy"] is not None and rec["rev_yoy"] <= 0)
                                 or (rec["op_income_yoy"] is not None and rec["op_income_yoy"] <= 0)),
            "earnings_ok": rec["bdays_to_earnings"] is None or rec["bdays_to_earnings"] >= 5,
        }
        # -8% stop is always available; wide_stop only flags that the structural stop is >15% away.
        if rec["rev_yoy"] is None or rec["op_income_yoy"] is None:
            rec["flags"].append("fin_unknown")
        rec["rs_rating"] = rs_rating.get(tk)
        rules.tidy_signals(market, rec)
        ok, why = rules.check(market, rec, regime)
        checks["backtest_rules"] = ok
        if not ok:
            rec["excluded_reason"] = why
        rec["checks"] = checks
        base = all(v for k, v in checks.items() if k not in ("trigger", "chase_ok"))
        rec["rank_hint"] = "A" if base and checks["trigger"] and checks["chase_ok"] else ("B" if base and not checks["trigger"] else None)
        rec["rs_excess"] = (m.ret_6m - bench_ret) if bench_ret is not None else None
        rec["rs_rating"] = rs_rating.get(tk)
        out.append(rec)

    out.sort(key=lambda r: rules.rank_key(market, r), reverse=True)
    result = {
        "generated_at": started.isoformat(timespec="seconds"),
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "market": market,
        "currency": cfg["ccy"],
        "data_date": max((r["date"] for r in out), default=None),
        "benchmark": {"ticker": cfg["bench"], "name": cfg["bench_name"], "ret_6m": bench_ret},
        "thresholds": {"min_turnover_20d": cfg["min_turnover"], "min_market_cap": cfg["min_mcap"]},
        "universe_size": int(len(uni)),
        "priced": len(prices),
        "liquid": len(rows),
        "passed_count": len(out),
        "counts": {"A": sum(r["rank_hint"] == "A" for r in out), "B": sum(r["rank_hint"] == "B" for r in out)},
        "note": "rank_hint is mechanical. Verify price, volume, earnings date and fundamentals before acting.",
        "market_regime": regime,
        "A": [r for r in out if r["rank_hint"] == "A"][:40],
        "B": [r for r in out if r["rank_hint"] == "B"][:40],
        "trigger_but_failed": [r for r in out if r["triggers"] and r["rank_hint"] != "A"][:40],
        "rules_note": "A/B also require the market-specific backtest rules in screener/rules.py (see excluded_reason)",
        "errors": errors[:300],
        "error_count": len(errors),
    }
    DATA.mkdir(exist_ok=True)
    (DATA / "history").mkdir(exist_ok=True)
    text = json.dumps(clean(result), ensure_ascii=False, indent=1, default=str)
    (DATA / f"{market}.json").write_text(text, encoding="utf-8")
    day = result["data_date"] or started.date().isoformat()
    slim = {k: result[k] for k in ("generated_at", "market", "data_date", "benchmark", "counts", "A", "B")}
    (DATA / "history" / f"{day}_{market}.json").write_text(
        json.dumps(clean(slim), ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    if _FIN_ERRORS:
        log("fundamentals errors (first 5): " + " | ".join(_FIN_ERRORS))
    known = sum(r["rev_yoy"] is not None for r in out)
    log(f"fundamentals known: {known}/{len(out)}")
    names = {t: v.get("name") for t, v in meta.items()}
    n_price = price_table.write(market, prices_all, names)
    log(f"price table: {n_price} tickers")
    log(f"done: A={result['counts']['A']} B={result['counts']['B']} errors={len(errors)}")
    return 0 if prices else 1


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--market", choices=["jp", "us"], required=True)
    sys.exit(main(p.parse_args().market))

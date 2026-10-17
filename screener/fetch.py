"""Daily OHLCV download that patches the most recent sessions from 60-minute bars.

Yahoo often leaves the latest Japanese daily bar with Close=NaN (or omits it for thin ETFs)
for many hours after the close, while the 60-minute bars are already complete. We rebuild
any session newer than the last valid daily close from the intraday bars.
"""
from __future__ import annotations

import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

import pandas as pd
import yfinance as yf

FIELDS = ["Open", "High", "Low", "Close", "Volume"]


def _log(*a):
    print(*a, file=sys.stderr, flush=True)


def _split(raw: pd.DataFrame, tickers: list[str]) -> dict[str, pd.DataFrame]:
    out = {}
    if raw is None or raw.empty:
        return out
    if isinstance(raw.columns, pd.MultiIndex):
        lv0 = set(raw.columns.get_level_values(0))
        for t in tickers:
            if t in lv0:
                out[t] = raw[t]
    else:
        out[tickers[0]] = raw
    return out


def _retry(fn, tries=3, wait=5):
    for k in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            if k == tries - 1:
                raise
            _log(f"retry after error: {e}")
            time.sleep(wait * (k + 1))


def _daily_from_intraday(h: pd.DataFrame) -> pd.DataFrame:
    h = h.dropna(subset=["Close"])
    if h.empty:
        return h
    idx = h.index.tz_convert(h.index.tz) if h.index.tz is not None else h.index
    day = pd.to_datetime(idx.date)
    g = h.groupby(day)
    d = pd.DataFrame({"Open": g["Open"].first(), "High": g["High"].max(), "Low": g["Low"].min(),
                      "Close": g["Close"].last(), "Volume": g["Volume"].sum()})
    return d


def patch(daily: pd.DataFrame, intraday: pd.DataFrame | None) -> pd.DataFrame:
    daily = daily[[c for c in FIELDS if c in daily.columns]].copy()
    if daily.index.tz is not None:
        daily.index = daily.index.tz_localize(None)
    if intraday is None or intraday.empty:
        return daily.dropna(subset=["Close"])
    valid = daily.dropna(subset=["Close"])
    last = valid.index.max() if not valid.empty else pd.Timestamp.min
    add = _daily_from_intraday(intraday)
    add = add[add.index > last]
    if add.empty:
        return valid
    return pd.concat([valid, add]).sort_index()


def _is_jp(t: str) -> bool:
    return t.endswith(".T") or t in ("^N225", "^TPX", "JPY=X")


def download(tickers: list[str], period: str = "2y", chunk: int = 150, auto_adjust: bool = True,
             intraday: bool = True) -> dict[str, pd.DataFrame]:
    """Download per exchange group: mixing time zones in one request shifts intraday timestamps."""
    out: dict[str, pd.DataFrame] = {}
    for group in ([t for t in tickers if _is_jp(t)], [t for t in tickers if not _is_jp(t)]):
        if group:
            out.update(_download_group(group, period, chunk, auto_adjust, intraday))
    return out


def _download_group(tickers: list[str], period: str, chunk: int, auto_adjust: bool,
                    intraday: bool) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    for s in range(0, len(tickers), chunk):
        part = tickers[s:s + chunk]
        d = _split(_retry(lambda: yf.download(part, period=period, interval="1d", auto_adjust=auto_adjust,
                                              group_by="ticker", threads=True, progress=False)), part)
        h = {}
        if intraday:
            try:
                h = _split(_retry(lambda: yf.download(part, period="5d", interval="60m", auto_adjust=auto_adjust,
                                                      group_by="ticker", threads=True, progress=False)), part)
            except Exception as e:  # noqa: BLE001
                _log(f"intraday failed for chunk {s}: {e}")
        for t in part:
            if t in d:
                try:
                    valid = d[t].dropna(subset=["Close"])
                    idx = valid.index.tz_localize(None) if valid.index.tz is not None else valid.index
                    valid_last = idx.max() if len(idx) else None
                    out[t] = patch(d[t], h.get(t))
                    if not out[t].empty and (valid_last is None or out[t].index.max() > valid_last):
                        out[t].attrs["close_source"] = "60m"
                except Exception as e:  # noqa: BLE001
                    _log(f"patch failed {t}: {e}")
                    out[t] = d[t].dropna(subset=["Close"])
        _log(f"downloaded {min(s + chunk, len(tickers))}/{len(tickers)}")
        time.sleep(1)
    rebuilt = [t for t, df in out.items() if df.attrs.get("close_source") == "60m"]
    if rebuilt:
        fixed = official_closes(out, rebuilt)
        _log(f"latest session rebuilt from 60m bars: {len(rebuilt)}, official close applied: {fixed}")
    return out


def _chart_meta(t: str) -> dict | None:
    """Yahoo chart meta. regularMarketPrice is the official last price, including the closing auction."""
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1d&interval=1d",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        m = r.json()["chart"]["result"][0]["meta"]
        ts = pd.Timestamp(m["regularMarketTime"], unit="s", tz="UTC").tz_convert(m.get("exchangeTimezoneName", "UTC"))
        return {"price": m.get("regularMarketPrice"), "volume": m.get("regularMarketVolume"),
                "high": m.get("regularMarketDayHigh"), "low": m.get("regularMarketDayLow"),
                "date": pd.Timestamp(ts.date())}
    except Exception:  # noqa: BLE001
        return None


def official_closes(data: dict[str, pd.DataFrame], tickers: list[str], workers: int = 12) -> int:
    """Replace the 60m-rebuilt latest session with Yahoo's official session values where available."""
    with ThreadPoolExecutor(max_workers=workers) as ex:
        metas = dict(zip(tickers, ex.map(_chart_meta, tickers)))
    fixed = 0
    for t, m in metas.items():
        df = data[t]
        if not m or not m.get("price") or df.empty or df.index[-1] != m["date"]:
            continue
        df = df.copy()
        df.iloc[-1, df.columns.get_loc("Close")] = float(m["price"])
        for col, key in (("Volume", "volume"), ("High", "high"), ("Low", "low")):
            if m.get(key) and col in df.columns:
                df.iloc[-1, df.columns.get_loc(col)] = float(m[key])
        df.attrs["close_source"] = "official"
        data[t] = df
        fixed += 1
    return fixed

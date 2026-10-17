"""Diagnose how fresh each free data source is for a few tickers (run from Actions)."""
import io, datetime as dt
import requests, pandas as pd, yfinance as yf

T = ["7203.T", "1306.T", "6758.T", "AAPL"]
print("utc now", dt.datetime.utcnow())
for t in T:
    print("=====", t)
    try:
        d = yf.download(t, period="5d", interval="1d", progress=False, auto_adjust=False)
        print("1d tail:\n", d.tail(3)[["Close"]] if not d.empty else "empty")
    except Exception as e: print("1d err", e)
    try:
        h = yf.download(t, period="2d", interval="60m", progress=False, auto_adjust=False)
        print("60m tail:\n", h.tail(2)[["Close"]] if not h.empty else "empty")
    except Exception as e: print("60m err", e)
    try:
        fi = yf.Ticker(t).fast_info
        print("fast_info last_price", fi.get("lastPrice"), "prev", fi.get("previousClose"))
    except Exception as e: print("fast_info err", e)
    try:
        r = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d",
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        m = r.json()["chart"]["result"][0]["meta"]
        print("chart meta", m.get("regularMarketPrice"), dt.datetime.utcfromtimestamp(m.get("regularMarketTime", 0)))
    except Exception as e: print("chart err", e)
    if t.endswith(".T"):
        s = t.replace(".T", ".jp").lower()
        try:
            r = requests.get(f"https://stooq.com/q/d/l/?s={s}&i=d", headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
            print("stooq status", r.status_code, r.text[-200:])
        except Exception as e: print("stooq err", e)

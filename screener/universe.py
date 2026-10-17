"""Universe builders. JP: JPX listed-issues file. US: S&P 500 + S&P 400 + Nasdaq-100 (Wikipedia)."""
from __future__ import annotations

import io
import re

import pandas as pd
import requests

UA = {"User-Agent": "Mozilla/5.0 (market-screener; personal research)"}
JPX_PAGE = "https://www.jpx.co.jp/markets/statistics-equities/misc/01.html"
JPX_FALLBACK = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xlsx"
JP_MARKETS = {"プライム（内国株式）", "スタンダード（内国株式）", "グロース（内国株式）"}
WIKI = [
    "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies",
    "https://en.wikipedia.org/wiki/Nasdaq-100",
]


def _jpx_file_url() -> str:
    """The listed-issues file has moved before (.xls -> .xlsx); read the link from the page."""
    try:
        page = requests.get(JPX_PAGE, headers=UA, timeout=60)
        page.raise_for_status()
        m = re.search(r'href="([^"]*data_j\.xlsx?)"', page.text)
        if m:
            return requests.compat.urljoin(JPX_PAGE, m.group(1))
    except requests.RequestException:
        pass
    return JPX_FALLBACK


def jp_universe() -> pd.DataFrame:
    url = _jpx_file_url()
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    df = pd.read_excel(io.BytesIO(r.content), dtype=str)
    df.columns = [str(c).strip() for c in df.columns]
    df = df[df["市場・商品区分"].isin(JP_MARKETS)]
    out = pd.DataFrame({
        "ticker": df["コード"].str.strip() + ".T",
        "code": df["コード"].str.strip(),
        "name": df["銘柄名"].str.strip(),
        "market": df["市場・商品区分"].str.replace("（内国株式）", "", regex=False),
        "sector": df.get("33業種区分", pd.Series([""] * len(df), index=df.index)),
    })
    return out.drop_duplicates("ticker").reset_index(drop=True)


def _symbol_table(html: str) -> pd.DataFrame | None:
    for t in pd.read_html(io.StringIO(html)):
        if isinstance(t.columns, pd.MultiIndex):
            t.columns = [" ".join(str(x) for x in c if "Unnamed" not in str(x)).strip() for c in t.columns]
        cols = {str(c).strip(): c for c in t.columns}
        sym = next((cols[k] for k in cols if k.split(" ")[0] in ("Symbol", "Ticker") or k == "Ticker symbol"), None)
        if sym is not None and len(t) >= 90:
            name = next((cols[k] for k in cols if k in ("Security", "Company", "Name")), None)
            sector = next((cols[k] for k in cols if "Sector" in k), None)
            return pd.DataFrame({
                "symbol": t[sym].astype(str).str.strip(),
                "name": t[name].astype(str) if name is not None else "",
                "sector": t[sector].astype(str) if sector is not None else "",
            })
    return None


def us_universe() -> pd.DataFrame:
    frames = []
    for url in WIKI:
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        t = _symbol_table(r.text)
        if t is None:
            print(f"warning: no symbol table found at {url}", flush=True)
            continue
        frames.append(t)
    if not frames:
        raise RuntimeError("no US universe could be built")
    df = pd.concat(frames).drop_duplicates("symbol")
    df["ticker"] = df["symbol"].str.replace(".", "-", regex=False)
    df["code"] = df["symbol"]
    df["market"] = "US"
    return df[["ticker", "code", "name", "market", "sector"]].reset_index(drop=True)

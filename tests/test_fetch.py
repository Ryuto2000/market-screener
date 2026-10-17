import numpy as np
import pandas as pd

from screener.fetch import patch


def test_patch_rebuilds_missing_session():
    d = pd.DataFrame({"Open": [1, 2, np.nan], "High": [1, 2, np.nan], "Low": [1, 2, np.nan],
                      "Close": [1.0, 2.0, np.nan], "Volume": [10, 10, np.nan]},
                     index=pd.to_datetime(["2026-10-14", "2026-10-15", "2026-10-16"]))
    idx = pd.DatetimeIndex(["2026-10-15 15:00", "2026-10-16 09:00", "2026-10-16 15:00"]).tz_localize("Asia/Tokyo")
    h = pd.DataFrame({"Open": [2, 3, 3.4], "High": [2, 3.2, 3.6], "Low": [2, 2.9, 3.3],
                      "Close": [2.0, 3.1, 3.55], "Volume": [5, 7, 8]}, index=idx)
    out = patch(d, h)
    assert list(out.index.strftime("%Y-%m-%d")) == ["2026-10-14", "2026-10-15", "2026-10-16"]
    last = out.iloc[-1]
    assert last["Close"] == 3.55 and last["Open"] == 3 and last["High"] == 3.6 and last["Volume"] == 15


def test_patch_no_intraday():
    d = pd.DataFrame({"Open": [1.0], "High": [1.0], "Low": [1.0], "Close": [1.0], "Volume": [1.0]},
                     index=pd.to_datetime(["2026-10-14"]))
    assert len(patch(d, None)) == 1


def test_official_close_overrides_rebuilt_session(monkeypatch):
    import screener.fetch as f
    df = pd.DataFrame({"Open": [1.0, 3.0], "High": [1.0, 3.6], "Low": [1.0, 2.9], "Close": [1.0, 3.54], "Volume": [1.0, 15.0]},
                      index=pd.to_datetime(["2026-10-15", "2026-10-16"]))
    df.attrs["close_source"] = "60m"
    monkeypatch.setattr(f, "_chart_meta", lambda t: {"price": 3.55, "volume": 20.0, "high": 3.6, "low": 2.9,
                                                     "date": pd.Timestamp("2026-10-16")})
    data = {"X.T": df}
    assert f.official_closes(data, ["X.T"]) == 1
    assert data["X.T"]["Close"].iloc[-1] == 3.55 and data["X.T"].attrs["close_source"] == "official"

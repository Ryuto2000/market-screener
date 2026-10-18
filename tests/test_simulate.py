import numpy as np
import pandas as pd

from screener import simulate as sim


def frame(opens, highs, lows, closes):
    idx = pd.bdate_range("2024-01-01", periods=len(closes))
    return pd.DataFrame({"Open": opens, "High": highs, "Low": lows, "Close": closes,
                         "Volume": np.full(len(closes), 1e6)}, index=idx)


def flat_then(path, pre=60):
    c = [100.0] * pre + list(path)
    o = [c[0]] + c[:-1]  # open at the previous close
    hi = [max(a, b) * 1.005 for a, b in zip(o, c)]
    lo = [min(a, b) * 0.995 for a, b in zip(o, c)]
    return frame(o, hi, lo, c)


def test_stop_hit_intraday():
    df = flat_then([100, 98, 95, 91, 90])
    r = sim.exit_rules(df, 60, "intraday")
    assert r["exit"] == "stop" and abs(r["ret"] + 0.08) < 1e-9


def test_close_stop_sells_next_open():
    df = flat_then([100, 98, 91, 90, 95])  # close 91 < 92 -> sell at the next open (= 91)
    r = sim.exit_rules(df, 60, "close")
    assert r["exit"] == "stop_close" and abs(r["ret"] + 0.09) < 1e-9


def test_trim_and_breakeven():
    # rally to +20% then collapse: 1/3 sold at the open after +16%, rest stopped at +8% or higher
    path = [100, 104, 109, 113, 117, 120, 121, 110, 100, 95]
    df = flat_then(path)
    r = sim.exit_rules(df, 60, "intraday")
    assert r["stage"] == 2
    assert r["ret"] > 0.08


def test_forward_horizons_and_first_hit():
    path = list(np.linspace(100, 130, 70))
    df = flat_then(path)
    f = sim.forward(df, 60)
    assert f["r5"] > 0 and f["first_hit"] == "target"
    assert f["mae60"] > -0.01

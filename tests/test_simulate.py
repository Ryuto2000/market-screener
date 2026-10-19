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


def test_trailing_from_high_with_add():
    # rally to +21% then collapse (80 flat sessions so the 3-month high exists): stop trails 10% under the high; half-size add at the open after +8%
    path = [100, 104, 109, 113, 117, 120, 121, 110, 100, 95]
    r = sim.exit_rules(flat_then(path, pre=80), 80, "intraday")
    assert r["added"] and r["stage"] == 1
    assert 0.08 < r["ret"] < 0.11


def test_breakeven_plus_one_and_add_loss():
    # +8.5% close -> stop to +1%, add 0.5x at 108.5; fall back -> initial +1%, add lot -3.75%
    r = sim.exit_rules(flat_then([100, 104, 108.5, 103, 100, 98], pre=80), 80, "intraday")
    assert r["exit"] == "stop" and abs(r["ret"] - (0.01 - 0.0375)) < 1e-4
    r0 = sim.exit_rules(flat_then([100, 104, 108.5, 103, 100, 98], pre=80), 80, "intraday", add=None)
    assert abs(r0["ret"] - 0.01) < 1e-9


def test_old_rules_trim():
    path = [100, 104, 109, 113, 117, 120, 121, 110, 100, 95]
    r = sim.exit_rules(flat_then(path), 60, "intraday", **sim.OLD_RULES)
    assert r["stage"] == 2 and r["ret"] > 0.08


def test_forward_horizons_and_first_hit():
    path = list(np.linspace(100, 130, 70))
    df = flat_then(path)
    f = sim.forward(df, 60)
    assert f["r5"] > 0 and f["first_hit"] == "target"
    assert f["mae60"] > -0.01


def test_earnings_exit_modes():
    path = [100, 102, 104, 103, 105, 104, 106, 105, 107, 108]
    df = flat_then(path, pre=80)
    e = [80 + 5]  # reaction on the 6th session after entry
    r_always = sim.exit_rules(df, 80, "close", earn_days=e, earn_mode="always")
    assert r_always["exit"] == "earnings" and abs(r_always["ret"] - 0.05) < 1e-9  # sold at the close before (105)
    r_be = sim.exit_rules(df, 80, "close", earn_days=e, earn_mode="unless_be")
    assert r_be["exit"] == "earnings"  # still below +8%, so it also sells
    r_none = sim.exit_rules(df, 80, "close")
    assert r_none["exit"] != "earnings"

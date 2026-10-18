import numpy as np

from screener import simulate as sim
from screener import variants as var
from tests.test_simulate import flat_then


def test_default_matches_simulate():
    rng = np.random.default_rng(0)
    for _ in range(40):
        path = list(100 * np.cumprod(1 + rng.normal(0.003, 0.03, 150)))
        df = flat_then(path)
        for mode in ("intraday", "close"):
            r = var.run(df, 60, mode)
            assert abs(r["ret"] - sim.exit_rules(df, 60, mode)["ret"]) < 1e-3
            assert not r["added"]


def test_wider_stop_survives_dip():
    df = flat_then([100, 95, 91, 93, 100, 110, 120, 125, 130] + [130] * 10)
    assert var.run(df, 60, "intraday", stop=0.08)["ret"] < 0
    assert var.run(df, 60, "intraday", stop=0.12)["ret"] > 0


def test_all_out_target():
    df = flat_then([100, 104, 108, 111, 115, 115, 115])
    r = var.run(df, 60, "intraday", full_at=0.10)
    assert abs(r["ret"] - 0.11) < 1e-9  # close 111 >= +10% -> sold at the next open (= 111)


def test_trailing_from_high():
    df = flat_then([100, 105, 110, 112, 106, 100])  # high ~112.6 after +8% -> stop ~107
    r = var.run(df, 60, "intraday", hi_trail=0.05, trim_at=None)
    assert 0.05 < r["ret"] < 0.08


def test_rebreak_add():
    # +8%, pull back 9%, then a new closing high -> add 0.5x at the next open
    path = [100, 104, 110, 106, 101, 105, 111, 113, 114, 115, 115]
    df = flat_then(path)
    r = var.run(df, 60, "intraday", add="rebreak", add_pb=0.08, add_frac=0.5, be_level=0.0)
    assert r["added"] and r["add_ret"] > 0
    base = var.run(df, 60, "intraday")
    assert r["ret"] > base["ret"]

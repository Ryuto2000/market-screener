import numpy as np

from screener import simulate as sim
from screener import variants as var
from tests.test_simulate import flat_then


def test_default_matches_simulate():
    rng = np.random.default_rng(0)
    for _ in range(30):
        path = list(100 * np.cumprod(1 + rng.normal(0.003, 0.03, 150)))
        df = flat_then(path)
        for mode in ("intraday", "close"):
            ret, _ = var.run(df, 60, mode)
            assert abs(ret - sim.exit_rules(df, 60, mode)["ret"]) < 1e-3


def test_wider_stop_survives_dip():
    df = flat_then([100, 95, 91, 93, 100, 110, 120, 125, 130] + [130] * 10)
    assert var.run(df, 60, "intraday", stop=0.08)[0] < 0
    assert var.run(df, 60, "intraday", stop=0.12)[0] > 0


def test_all_out_target():
    df = flat_then([100, 104, 108, 111, 115, 115, 115])
    ret, _ = var.run(df, 60, "intraday", full_at=0.10)
    assert abs(ret - 0.11) < 1e-9  # close 111 >= +10% -> sold at the next open (= 111)

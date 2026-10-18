import numpy as np

from screener import simulate as sim
from screener import variants as var
from tests.test_simulate import flat_then


def test_old_rules_reproduce_previous_ladder():
    # previous ladder: +20% then collapse -> 1/3 trimmed, rest stopped at >= +8%
    df = flat_then([100, 104, 109, 113, 117, 120, 121, 110, 100, 95])
    r = var.run(df, 60, "intraday", **sim.OLD_RULES)
    assert r["stage"] == 2 and r["ret"] > 0.08 and not r["added"]


def test_variants_cover_current():
    assert var.VARIANTS["current vs previous"][var.CUR] == sim.RULES


def test_wider_stop_survives_dip():
    df = flat_then([100, 95, 91, 93, 100, 110, 120, 125, 130] + [130] * 10)
    assert var.run(df, 60, "intraday", **var._v(stop=0.08))["ret"] < 0
    assert var.run(df, 60, "intraday", **var._v(stop=0.12))["ret"] > 0


def test_rebreak_add():
    path = [100, 104, 110, 106, 101, 105, 111, 113, 114, 115, 115]
    df = flat_then(path)
    r = var.run(df, 60, "intraday", **var._v(add="rebreak", add_pb=0.08, be_level=0.0, hi_trail=None))
    assert r["added"] and r["add_ret"] > 0


def test_random_paths_run():
    rng = np.random.default_rng(0)
    for _ in range(30):
        df = flat_then(list(100 * np.cumprod(1 + rng.normal(0.003, 0.03, 150))))
        for grp in var.VARIANTS.values():
            for kw in grp.values():
                for mode in ("intraday", "close"):
                    r = var.run(df, 60, mode, **kw)
                    assert r["ret"] > -0.5

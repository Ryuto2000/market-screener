from screener import rules


def test_jp_exclusions():
    assert not rules.check("jp", {"flags": ["stop_inside_noise"], "rs_rating": 60}, None)[0]
    assert not rules.check("jp", {"flags": ["deep_base"], "rs_rating": 60}, None)[0]
    assert not rules.check("jp", {"flags": [], "rs_rating": 97}, None)[0]
    assert rules.check("jp", {"flags": ["macd_divergence"], "rs_rating": 81}, None)[0]


def test_us_requires_strength_and_regime():
    up = {"benchmark_state": "uptrend", "benchmark_distribution_days_25": 2}
    assert rules.check("us", {"flags": [], "rs_rating": 91}, up)[0]
    assert not rules.check("us", {"flags": [], "rs_rating": 85}, up)[0]
    assert not rules.check("us", {"flags": [], "rs_rating": 95}, {**up, "benchmark_distribution_days_25": 5})[0]
    assert not rules.check("us", {"flags": [], "rs_rating": 95}, {**up, "benchmark_state": "mixed"})[0]


def test_jp_power_gap_is_info():
    rec = {"plus": ["power_gap", "accumulation"]}
    rules.tidy_signals("jp", rec)
    assert rec["plus"] == ["accumulation"] and rec["info"] == ["power_gap"]


def test_risk_per_trade_breadth():
    assert rules.risk_per_trade("jp", {"pct_above_sma50": 80}) == 0.005
    assert rules.risk_per_trade("jp", {"pct_above_sma50": 74.9}) == 0.003
    assert rules.risk_per_trade("us", {"pct_above_sma50": 90}) == 0.003
    assert rules.risk_per_trade("jp", None) == 0.003


def test_pinned_price_excluded_both_markets():
    rec = {"flags": ["pinned_price"], "rs_rating": 92}
    assert not rules.check("jp", rec, None)[0]
    assert not rules.check("us", rec, {"benchmark_state": "uptrend"})[0]

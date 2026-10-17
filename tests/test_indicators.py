import numpy as np
import pandas as pd

from screener import indicators as ind


def frame(closes, vols=None, spread=0.005):
    closes = np.asarray(closes, dtype=float)
    idx = pd.bdate_range("2024-01-01", periods=len(closes))
    vols = np.full(len(closes), 1_000_000.0) if vols is None else np.asarray(vols, dtype=float)
    opens = np.r_[closes[0], closes[:-1]]
    return pd.DataFrame({
        "Open": opens,
        "High": np.maximum(opens, closes) * (1 + spread),
        "Low": np.minimum(opens, closes) * (1 - spread),
        "Close": closes,
        "Volume": vols,
    }, index=idx)


def uptrend(n=300, start=100, drift=0.002):
    return start * np.cumprod(np.full(n, 1 + drift))


def test_short_history_rejected():
    m = ind.compute(frame(uptrend(150)), 0.0)
    assert not m.ok


def test_trend_and_rs():
    m = ind.compute(frame(uptrend()), 0.05)
    assert m.ok and m.trend_ok
    m2 = ind.compute(frame(uptrend()), 5.0)  # benchmark did better
    assert not m2.trend_ok


def test_downtrend_fails():
    m = ind.compute(frame(uptrend(drift=-0.002)), -1.0)
    assert not m.trend_ok


def test_breakout_with_volume():
    c = list(uptrend(280, drift=0.001))
    # flat base for 60 days, then breakout on 3x volume today
    base = c[-1]
    c += [base * (1 + 0.002 * np.sin(i)) for i in range(60)]
    c.append(base * 1.06)
    v = [1e6] * (len(c) - 1) + [3e6]
    m = ind.compute(frame(c, v), -1.0)
    assert "a_breakout" in m.triggers
    assert m.chase_ok is False or m.entry_limit >= m.breakout_level  # entry limit = level +3%
    assert abs(m.entry_limit / m.breakout_level - 1.03) < 1e-9


def test_breakout_without_volume_is_not_a():
    c = list(uptrend(280, drift=0.001))
    base = c[-1]
    c += [base] * 60 + [base * 1.06]
    m = ind.compute(frame(c), -1.0)
    assert "a_breakout" not in m.triggers
    assert "b_near_high" in m.triggers


def test_pullback_reentry():
    c = list(uptrend(280, drift=0.001))
    base = c[-1]
    c += [base] * 60
    c += [base * 1.08, base * 1.10, base * 1.07, base * 1.04, base * 1.01, base * 1.005, base * 1.03]
    v = [1e6] * len(c)
    v[-7] = 3e6
    m = ind.compute(frame(c, v), -1.0)
    assert "c_pullback" in m.triggers, m.triggers


def test_stop_struct_below_close():
    m = ind.compute(frame(uptrend()), 0.0)
    assert m.stop_struct is None or m.stop_struct < m.close
    assert abs(m.stop_8pct / m.close - 0.92) < 1e-9


def test_secondary_indicators_present():
    m = ind.compute(frame(uptrend()), 0.0)
    assert 0 <= m.rsi14 <= 100
    assert m.macd > 0 and not np.isnan(m.macd_hist)
    assert not np.isnan(m.bb_pctb)


def test_heavy_selling_day_flag():
    c = list(uptrend(300, drift=0.002))
    df = frame(c)
    # last bar: opened high, closed near the low on 2x volume
    df.iloc[-1, df.columns.get_loc("Open")] = c[-1] * 1.03
    df.iloc[-1, df.columns.get_loc("High")] = c[-1] * 1.035
    df.iloc[-1, df.columns.get_loc("Low")] = c[-1] * 0.998
    df.iloc[-1, df.columns.get_loc("Volume")] = 2e6
    m = ind.compute(df, 0.0)
    assert "heavy_selling_day" in m.flags, m.flags


def test_overheat_flag_on_steep_rise():
    m = ind.compute(frame(uptrend(300, drift=0.01)), 0.0)
    assert "overheat" in m.flags


def test_bearish_divergence():
    # strong rally to a peak, pullback, then a slow grind to a marginally higher high
    c = list(uptrend(200, drift=0.001))
    p = c[-1]
    c += [p * (1 + 0.012 * i) for i in range(1, 31)]          # fast rally
    top = c[-1]
    c += [top * (1 - 0.004 * i) for i in range(1, 41)]        # pullback
    low = c[-1]
    c += [low + (top * 1.01 - low) * i / 40 for i in range(1, 41)]  # slow climb to a new high
    assert ind._bearish_divergence(pd.Series(c), ind.macd(pd.Series(c))[0])

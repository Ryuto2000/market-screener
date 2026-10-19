import numpy as np
import pandas as pd

from screener import earnings


def test_reaction_day_in_season():
    idx = pd.bdate_range("2024-01-01", "2024-12-31")
    v = np.full(len(idx), 1e6)
    spike = idx.get_loc(pd.Timestamp("2024-05-10"))
    v[spike] = 5e6
    df = pd.DataFrame({"Close": 100.0, "Volume": v}, index=idx)
    days = earnings.reaction_days(df, "jp")
    assert spike in days

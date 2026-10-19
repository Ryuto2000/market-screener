"""Estimated earnings reaction sessions from price and volume (no point-in-time earnings calendar).

Within each reporting season the session with the highest volume relative to its 50-day average
(at least 2x) is taken as the reaction to the quarterly results. Japanese seasons cluster in
late Jan-Feb, late Apr-May, late Jul-Aug and late Oct-Nov; US seasons are similar but start earlier.
This is an estimate: results outside the seasons or without a volume spike are missed.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SEASONS = {
    "jp": [((1, 25), (2, 20)), ((4, 20), (5, 20)), ((7, 20), (8, 20)), ((10, 20), (11, 20))],
    "us": [((1, 12), (3, 5)), ((4, 10), (5, 25)), ((7, 10), (8, 25)), ((10, 10), (11, 25))],
}
MIN_RATIO = 2.0


def reaction_days(df: pd.DataFrame, market: str) -> np.ndarray:
    v = df["Volume"]
    ratio = (v / v.rolling(50).mean().shift(1)).to_numpy(float)
    md = df.index.month * 100 + df.index.day
    years = df.index.year
    out = []
    for y in np.unique(years):
        for (m1, d1), (m2, d2) in SEASONS[market]:
            mask = (years == y) & (md >= m1 * 100 + d1) & (md <= m2 * 100 + d2)
            idx = np.flatnonzero(mask)
            if not len(idx):
                continue
            r = ratio[idx]
            if np.all(np.isnan(r)):
                continue
            k = idx[int(np.nanargmax(r))]
            if ratio[k] >= MIN_RATIO:
                out.append(k)
    return np.array(sorted(out), dtype=int)

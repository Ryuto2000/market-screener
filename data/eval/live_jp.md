# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-10-30
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 393

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 241 | -1.1% | -1.1% | 34% | -4.5% | 2.8% |
| 10d | 41 | -1.9% | -1.7% | 29% | -7.5% | 5.1% |

First within 60 sessions: -8% stop 24, +16% 0, neither 369. Median MFE 1.5%, median MAE -3.2%, MAE p10 -7.2%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 393 | 32% | 2.3% | -2.3% | -0.84% | 0.47 | 4.0/3.0 | 65% |
| close stop | 393 | 32% | 2.3% | -2.3% | -0.84% | 0.47 | 4.0/3.0 | 65% |

Add-on: intraday: added in 1%, add lot mean 0.30% of the initial position; close: added in 1%, add lot mean 0.30% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 393 | 32% | -0.84% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 82 | 39% | -0.63% | None |
| 80-89 | 96 | 31% | -0.87% | None |
| 90-99 | 10 (small) | 40% | -2.12% | None |
| <70 | 204 | 29% | -0.85% | None |
| unknown | 1 (small) | 0% | -0.28% | None |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 160 | 37% | -0.72% | -0.92% | +0.20% | 6% |
| plus:accumulation | 160 | 28% | -0.94% | -0.77% | -0.17% | 6% |
| flags:macd_fading | 88 | 43% | -0.16% | -1.04% | +0.88% | 3% |
| flags:above_upper_band | 58 | 29% | -1.13% | -0.79% | -0.34% | 3% |
| plus:tight_base | 53 | 23% | -0.94% | -0.83% | -0.12% | 2% |
| flags:heavy_selling_day | 12 (small) | 50% | -0.17% | -0.86% | +0.70% | 0% |
| flags:volume_spike_5x | 8 (small) | 50% | 0.30% | -0.87% | +1.16% | 0% |
| flags:distribution | 5 (small) | 60% | 0.56% | -0.86% | +1.42% | 0% |
| flags:macd_dead_cross | 5 (small) | 20% | -1.09% | -0.84% | -0.25% | 0% |

## B-candidates (no trigger yet)

n=397, 20d mean None, rules expectancy -0.0073

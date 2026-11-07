# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-11-06
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 553

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 393 | -1.7% | -1.5% | 31% | -6.0% | 3.1% |
| 10d | 201 | -1.9% | -1.8% | 30% | -8.8% | 5.4% |

First within 60 sessions: -8% stop 143, +16% 7, neither 403. Median MFE 2.6%, median MAE -5.0%, MAE p10 -12.4%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 553 | 24% | 2.0% | -3.9% | -2.45% | 0.17 | 5.0/4.0 | 75% |
| close stop | 553 | 24% | 2.0% | -4.0% | -2.53% | 0.16 | 5.0/4.0 | 75% |

Add-on: intraday: added in 5%, add lot mean -2.43% of the initial position; close: added in 5%, add lot mean -2.55% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 553 | 24% | -2.45% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 122 | 32% | -2.68% | None |
| 80-89 | 129 | 16% | -3.57% | None |
| 90-99 | 17 (small) | 18% | -5.44% | None |
| <70 | 284 | 25% | -1.67% | None |
| unknown | 1 (small) | 100% | 0.36% | None |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| plus:accumulation | 214 | 22% | -2.42% | -2.46% | +0.04% | 26% |
| flags:macd_divergence | 201 | 27% | -2.19% | -2.59% | +0.40% | 23% |
| flags:macd_fading | 105 | 29% | -2.99% | -2.32% | -0.68% | 27% |
| flags:above_upper_band | 102 | 24% | -2.19% | -2.50% | +0.32% | 18% |
| plus:tight_base | 58 | 12% | -2.16% | -2.48% | +0.32% | 14% |
| flags:heavy_selling_day | 15 (small) | 27% | -2.83% | -2.43% | -0.40% | 20% |
| flags:macd_dead_cross | 9 (small) | 11% | -4.71% | -2.41% | -2.30% | 33% |
| flags:distribution | 8 (small) | 38% | -2.13% | -2.45% | +0.32% | 12% |
| flags:volume_spike_5x | 8 (small) | 38% | -4.36% | -2.42% | -1.95% | 50% |

## B-candidates (no trigger yet)

n=560, 20d mean None, rules expectancy -0.0203

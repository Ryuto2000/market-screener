# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-11-27
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 1113

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 953 | -0.4% | -0.3% | 44% | -4.9% | 4.7% |
| 10d | 753 | -0.3% | -0.5% | 46% | -7.0% | 7.6% |
| 20d | 353 | -1.6% | -1.6% | 39% | -11.9% | 9.4% |

First within 60 sessions: -8% stop 226, +16% 37, neither 850. Median MFE 3.5%, median MAE -3.5%, MAE p10 -10.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 1113 | 41% | 4.0% | -3.4% | -0.37% | 0.82 | 5.0/5.0 | 61% |
| close stop | 1113 | 41% | 4.0% | -3.5% | -0.38% | 0.82 | 5.0/6.0 | 60% |

Add-on: intraday: added in 10%, add lot mean -0.30% of the initial position; close: added in 10%, add lot mean -0.23% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 1113 | 41% | -0.37% | -1.6% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 283 | 43% | 0.04% | -0.1% |
| 80-89 | 289 | 48% | 0.06% | -3.2% |
| 90-99 | 69 | 48% | -0.94% | -8.5% |
| <70 | 471 | 34% | -0.80% | -1.2% |
| unknown | 1 (small) | 100% | 0.36% | 2.8% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 343 | 40% | -0.53% | -0.30% | -0.23% | 22% |
| plus:accumulation | 316 | 41% | -0.06% | -0.50% | +0.44% | 25% |
| flags:macd_fading | 228 | 39% | -0.13% | -0.43% | +0.30% | 16% |
| flags:above_upper_band | 213 | 49% | -0.21% | -0.41% | +0.21% | 19% |
| plus:tight_base | 73 | 30% | 0.13% | -0.41% | +0.54% | 16% |
| flags:heavy_selling_day | 43 | 49% | 0.42% | -0.40% | +0.82% | 19% |
| flags:distribution | 35 | 43% | 0.67% | -0.40% | +1.07% | 3% |
| flags:macd_dead_cross | 18 (small) | 33% | -1.13% | -0.36% | -0.77% | 28% |
| flags:volume_spike_5x | 10 (small) | 40% | -3.29% | -0.34% | -2.95% | 50% |
| flags:wide_stop | 1 (small) | 100% | 1.07% | -0.37% | +1.44% | 0% |

## B-candidates (no trigger yet)

n=1113, 20d mean 0.0175, rules expectancy 0.0035

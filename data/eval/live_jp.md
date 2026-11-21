# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-11-20
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 949

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 792 | -0.4% | -0.4% | 44% | -5.1% | 5.0% |
| 10d | 593 | -0.7% | -1.0% | 43% | -7.5% | 7.6% |
| 20d | 201 | -1.5% | -1.2% | 42% | -12.1% | 8.5% |

First within 60 sessions: -8% stop 209, +16% 18, neither 722. Median MFE 3.1%, median MAE -3.7%, MAE p10 -11.2%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 949 | 40% | 3.5% | -3.7% | -0.84% | 0.62 | 5.0/5.0 | 60% |
| close stop | 949 | 40% | 3.5% | -3.8% | -0.90% | 0.60 | 5.0/5.0 | 59% |

Add-on: intraday: added in 7%, add lot mean -0.64% of the initial position; close: added in 7%, add lot mean -0.58% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 949 | 40% | -0.84% | -1.5% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 233 | 41% | -0.75% | -1.1% |
| 80-89 | 232 | 44% | -0.98% | -1.7% |
| 90-99 | 44 | 39% | -2.39% | 0.1% |
| <70 | 439 | 37% | -0.67% | -1.7% |
| unknown | 1 (small) | 100% | 0.36% | 2.8% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 323 | 37% | -0.95% | -0.79% | -0.15% | 23% |
| plus:accumulation | 270 | 38% | -0.87% | -0.83% | -0.04% | 28% |
| flags:above_upper_band | 204 | 42% | -0.70% | -0.88% | +0.18% | 18% |
| flags:macd_fading | 167 | 45% | -0.71% | -0.87% | +0.17% | 21% |
| plus:tight_base | 59 | 36% | -0.26% | -0.88% | +0.62% | 20% |
| flags:heavy_selling_day | 39 | 46% | -0.29% | -0.87% | +0.58% | 15% |
| flags:distribution | 33 | 48% | 0.88% | -0.91% | +1.79% | 3% |
| flags:macd_dead_cross | 13 (small) | 31% | -2.15% | -0.83% | -1.32% | 38% |
| flags:volume_spike_5x | 10 (small) | 40% | -2.82% | -0.82% | -2.00% | 40% |
| flags:wide_stop | 1 (small) | 0% | -3.82% | -0.84% | -2.98% | 0% |

## B-candidates (no trigger yet)

n=948, 20d mean 0.015, rules expectancy -0.0048

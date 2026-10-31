# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-27 to 2026-10-28, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2571

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2569 | 0.0% | -0.2% | 47% | -5.3% | 5.5% |
| 10d | 2564 | 0.4% | 0.1% | 51% | -7.0% | 7.8% |
| 20d | 2542 | 1.2% | 0.6% | 53% | -9.0% | 11.9% |
| 40d | 2512 | 2.9% | 2.1% | 57% | -11.5% | 17.8% |
| 60d | 2461 | 4.5% | 3.1% | 59% | -14.1% | 23.8% |

First within 60 sessions: -8% stop 1197, +16% 724, neither 650. Median MFE 11.6%, median MAE -7.7%, MAE p10 -21.5%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2571 | 43% | 15.5% | -6.2% | 3.10% | 1.87 | 40.0/16.0 | 69% |
| close stop | 2571 | 44% | 17.8% | -7.0% | 3.78% | 1.95 | 46.0/21.0 | 70% |

Add-on: intraday: added in 39%, add lot mean 1.60% of the initial position; close: added in 40%, add lot mean 2.07% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 106 | 31% | -2.47% | -0.7% |
| 2023 | 737 | 44% | 3.13% | 1.1% |
| 2024 | 576 | 35% | -0.08% | 1.1% |
| 2025 | 710 | 53% | 8.65% | 2.0% |
| 2026 | 442 | 37% | -0.39% | 0.8% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 498 | 41% | 1.90% | 1.8% |
| uptrend | 2035 | 43% | 3.40% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1056 | 43% | 2.29% | 1.2% |
| >=5 | 1515 | 43% | 3.66% | 1.2% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 727 | 45% | 3.58% | 1.2% |
| 80-89 | 697 | 42% | 3.43% | 1.7% |
| 90-99 | 144 | 38% | 2.19% | 0.1% |
| <70 | 1003 | 42% | 2.65% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 49 | 39% | 4.38% | 1.0% |
| -2..-1% | 124 | 40% | 2.51% | 0.1% |
| -1..+1% | 2177 | 43% | 3.02% | 1.2% |
| +1..+2% | 198 | 45% | 4.48% | 2.7% |
| >=+2% | 23 | 43% | -0.71% | -2.7% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 83 | 35% | 0.48% | 1.2% |
| -2..0% | 959 | 45% | 3.90% | 1.8% |
| 0..+2% | 1404 | 42% | 2.68% | 0.8% |
| +2..+4% | 92 | 41% | 3.46% | 0.6% |
| >=+4% | 33 | 45% | 2.98% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 244 | 47% | 4.76% | 2.5% |
| 45-60% | 743 | 39% | 2.71% | 1.3% |
| 60-75% | 1090 | 42% | 2.04% | 0.7% |
| >=75% | 494 | 48% | 5.21% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1935 | 43% | 3.49% | 1.90% | +1.60% | 46% |
| flags:macd_divergence | 1269 | 43% | 3.76% | 2.45% | +1.32% | 46% |
| plus:accumulation | 1244 | 44% | 3.22% | 2.98% | +0.24% | 46% |
| plus:power_gap | 452 | 41% | 2.87% | 3.15% | -0.28% | 48% |
| plus:tight_base | 243 | 43% | 3.18% | 3.09% | +0.09% | 44% |
| flags:heavy_selling_day | 121 | 41% | 1.86% | 3.16% | -1.30% | 41% |
| flags:volume_spike_5x | 93 | 44% | 4.48% | 3.05% | +1.43% | 47% |
| flags:macd_fading | 29 | 31% | 0.06% | 3.13% | -3.07% | 59% |
| flags:distribution | 12 (small) | 50% | 3.84% | 3.09% | +0.75% | 42% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2571 | 43% / 44% | 3.10% | 3.78% | 1.2% | -2.9% / 3.8% / -0.8% / 10.7% / 0.2% |
| (b) within 3% of the 3-month high, next open | 8566 | 44% / 45% | 3.32% | 4.03% | 1.4% | -0.4% / 4.0% / -1.4% / 11.6% / 0.1% |
| (b) same, buy-stop above the high within 5 sessions | 4914 | 42% / 43% | 3.16% | 3.89% | 1.2% | -2.8% / 2.9% / -1.4% / 12.3% / 0.2% |
| (c) pullback re-entry, next open | 4457 | 46% / 47% | 3.54% | 4.28% | 1.8% | -0.8% / 3.8% / -2.0% / 11.7% / 0.5% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4365

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4359 | -0.0% | -0.3% | 47% | -7.3% | 6.9% |
| 10d | 4350 | 0.4% | -0.1% | 49% | -9.4% | 9.6% |
| 20d | 4313 | 0.9% | 0.0% | 50% | -13.2% | 14.2% |
| 40d | 4255 | 2.4% | 1.1% | 53% | -16.2% | 21.3% |
| 60d | 4158 | 4.1% | 2.0% | 55% | -19.8% | 29.3% |

First within 60 sessions: -8% stop 2328, +16% 1248, neither 789. Median MFE 13.0%, median MAE -9.7%, MAE p10 -28.1%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4365 | 39% | 15.5% | -6.5% | 2.10% | 1.53 | 31.5/11.0 | 72% |
| close stop | 4365 | 40% | 18.9% | -7.7% | 2.90% | 1.63 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.23% of the initial position; close: added in 40%, add lot mean 1.75% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 167 | 28% | -2.94% | -1.2% |
| 2023 | 1134 | 40% | 2.25% | 0.4% |
| 2024 | 929 | 33% | -0.65% | 0.2% |
| 2025 | 1122 | 49% | 7.55% | 2.2% |
| 2026 | 1013 | 34% | -0.77% | 0.9% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 823 | 39% | 1.15% | 0.9% |
| uptrend | 3482 | 39% | 2.31% | 0.8% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1754 | 39% | 1.81% | 0.9% |
| >=5 | 2611 | 39% | 2.29% | 0.8% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 899 | 43% | 3.24% | 1.2% |
| 80-89 | 1137 | 40% | 2.66% | 1.6% |
| 90-99 | 1215 | 33% | 0.45% | -0.1% |
| <70 | 1114 | 42% | 2.39% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 86 | 35% | 3.12% | -0.3% |
| -2..-1% | 225 | 36% | 1.09% | -0.3% |
| -1..+1% | 3675 | 39% | 2.02% | 0.8% |
| +1..+2% | 326 | 44% | 3.64% | 2.2% |
| >=+2% | 52 | 46% | 0.86% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 239 | 37% | 0.86% | 0.4% |
| -2..0% | 1528 | 41% | 2.80% | 1.8% |
| 0..+2% | 2230 | 40% | 1.99% | 0.6% |
| +2..+4% | 231 | 33% | 0.95% | -0.8% |
| >=+4% | 137 | 31% | 0.10% | -2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 411 | 43% | 3.18% | 3.1% |
| 45-60% | 1289 | 35% | 0.97% | 0.2% |
| 60-75% | 1751 | 40% | 2.21% | 0.8% |
| >=75% | 914 | 41% | 2.99% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3233 | 40% | 2.28% | 1.57% | +0.71% | 52% |
| plus:accumulation | 2504 | 39% | 2.21% | 1.95% | +0.26% | 54% |
| flags:macd_divergence | 1836 | 39% | 2.73% | 1.64% | +1.08% | 52% |
| flags:overheat | 1589 | 34% | 0.43% | 3.05% | -2.62% | 63% |
| plus:power_gap | 1173 | 36% | 1.50% | 2.32% | -0.82% | 59% |
| flags:deep_base | 866 | 29% | -0.18% | 2.66% | -2.84% | 70% |
| flags:stop_inside_noise | 851 | 28% | -0.37% | 2.69% | -3.06% | 70% |
| flags:volume_spike_5x | 265 | 36% | 0.88% | 2.18% | -1.30% | 58% |
| plus:tight_base | 256 | 43% | 2.93% | 2.05% | +0.88% | 44% |
| flags:heavy_selling_day | 192 | 38% | 1.29% | 2.13% | -0.85% | 51% |
| flags:macd_fading | 77 | 39% | 3.64% | 2.07% | +1.57% | 55% |
| flags:distribution | 14 (small) | 50% | 2.79% | 2.09% | +0.70% | 50% |

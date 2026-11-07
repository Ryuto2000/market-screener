# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-30 to 2026-11-05, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2610

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2581 | 0.0% | -0.2% | 47% | -5.3% | 5.5% |
| 10d | 2577 | 0.4% | 0.1% | 51% | -7.0% | 7.9% |
| 20d | 2556 | 1.2% | 0.6% | 53% | -9.0% | 11.9% |
| 40d | 2529 | 2.9% | 2.0% | 57% | -11.5% | 17.7% |
| 60d | 2479 | 4.5% | 3.1% | 59% | -14.1% | 23.8% |

First within 60 sessions: -8% stop 1209, +16% 729, neither 672. Median MFE 11.5%, median MAE -7.7%, MAE p10 -21.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2610 | 42% | 15.5% | -6.2% | 2.96% | 1.83 | 40.0/16.0 | 70% |
| close stop | 2610 | 43% | 17.7% | -7.0% | 3.61% | 1.90 | 46.0/21.0 | 71% |

Add-on: intraday: added in 39%, add lot mean 1.56% of the initial position; close: added in 40%, add lot mean 1.99% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 106 | 30% | -2.59% | -0.8% |
| 2023 | 740 | 44% | 3.11% | 1.1% |
| 2024 | 580 | 36% | -0.04% | 1.1% |
| 2025 | 711 | 53% | 8.62% | 1.9% |
| 2026 | 473 | 34% | -0.85% | 0.7% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 528 | 39% | 1.52% | 1.7% |
| uptrend | 2044 | 43% | 3.34% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1060 | 43% | 2.24% | 1.3% |
| >=5 | 1550 | 42% | 3.45% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 735 | 44% | 3.40% | 1.2% |
| 80-89 | 704 | 42% | 3.30% | 1.7% |
| 90-99 | 148 | 39% | 2.20% | 0.3% |
| <70 | 1023 | 42% | 2.52% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 69 | 28% | 1.96% | 1.0% |
| -2..-1% | 126 | 40% | 2.46% | 0.4% |
| -1..+1% | 2194 | 43% | 2.93% | 1.2% |
| +1..+2% | 198 | 44% | 4.41% | 2.5% |
| >=+2% | 23 | 43% | -0.71% | -2.7% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 89 | 33% | 0.23% | 1.2% |
| -2..0% | 977 | 44% | 3.69% | 1.8% |
| 0..+2% | 1417 | 42% | 2.60% | 0.8% |
| +2..+4% | 94 | 40% | 3.37% | 0.6% |
| >=+4% | 33 | 45% | 2.98% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 270 | 43% | 3.82% | 2.4% |
| 45-60% | 747 | 39% | 2.66% | 1.3% |
| 60-75% | 1097 | 42% | 1.95% | 0.7% |
| >=75% | 496 | 48% | 5.17% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1967 | 43% | 3.35% | 1.77% | +1.58% | 45% |
| flags:macd_divergence | 1284 | 42% | 3.64% | 2.30% | +1.35% | 46% |
| plus:accumulation | 1260 | 44% | 3.10% | 2.83% | +0.27% | 46% |
| plus:power_gap | 457 | 41% | 2.79% | 3.00% | -0.21% | 48% |
| plus:tight_base | 244 | 42% | 3.04% | 2.95% | +0.09% | 45% |
| flags:heavy_selling_day | 121 | 40% | 1.83% | 3.02% | -1.18% | 41% |
| flags:volume_spike_5x | 93 | 43% | 4.33% | 2.91% | +1.42% | 47% |
| flags:macd_fading | 28 | 25% | -1.39% | 3.01% | -4.40% | 64% |
| flags:distribution | 13 (small) | 46% | 3.32% | 2.96% | +0.36% | 38% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2610 | 42% / 43% | 2.96% | 3.61% | 1.2% | -3.0% / 3.8% / -0.7% / 10.6% / -0.4% |
| (b) within 3% of the 3-month high, next open | 8607 | 44% / 44% | 3.25% | 3.93% | 1.4% | -0.4% / 4.0% / -1.4% / 11.6% / -0.4% |
| (b) same, buy-stop above the high within 5 sessions | 4950 | 42% / 43% | 3.08% | 3.79% | 1.2% | -2.8% / 2.9% / -1.3% / 12.3% / -0.2% |
| (c) pullback re-entry, next open | 4437 | 46% / 46% | 3.49% | 4.20% | 1.8% | -1.1% / 3.8% / -2.0% / 11.7% / -0.2% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4408

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4374 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4366 | 0.4% | -0.1% | 49% | -9.4% | 9.5% |
| 20d | 4329 | 0.8% | 0.0% | 50% | -13.3% | 14.1% |
| 40d | 4275 | 2.4% | 1.0% | 53% | -16.2% | 21.2% |
| 60d | 4186 | 4.0% | 1.8% | 55% | -19.9% | 29.2% |

First within 60 sessions: -8% stop 2345, +16% 1253, neither 810. Median MFE 13.0%, median MAE -9.7%, MAE p10 -28.5%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4408 | 39% | 15.5% | -6.5% | 2.02% | 1.51 | 32.0/11.0 | 72% |
| close stop | 4408 | 40% | 18.8% | -7.7% | 2.80% | 1.60 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.20% of the initial position; close: added in 40%, add lot mean 1.71% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 166 | 27% | -3.05% | -1.4% |
| 2023 | 1137 | 40% | 2.24% | 0.4% |
| 2024 | 934 | 33% | -0.63% | 0.2% |
| 2025 | 1123 | 49% | 7.54% | 2.2% |
| 2026 | 1048 | 33% | -0.98% | 0.7% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 857 | 38% | 0.93% | 0.9% |
| uptrend | 3491 | 39% | 2.27% | 0.8% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1758 | 39% | 1.79% | 0.9% |
| >=5 | 2650 | 39% | 2.17% | 0.8% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 906 | 43% | 3.08% | 1.2% |
| 80-89 | 1145 | 40% | 2.62% | 1.6% |
| 90-99 | 1222 | 33% | 0.43% | -0.1% |
| <70 | 1135 | 41% | 2.28% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 107 | 29% | 1.80% | -0.3% |
| -2..-1% | 227 | 37% | 1.06% | -0.2% |
| -1..+1% | 3695 | 39% | 1.96% | 0.8% |
| +1..+2% | 326 | 43% | 3.60% | 2.1% |
| >=+2% | 52 | 46% | 0.86% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 246 | 37% | 0.77% | 0.3% |
| -2..0% | 1545 | 40% | 2.69% | 1.8% |
| 0..+2% | 2246 | 39% | 1.93% | 0.6% |
| +2..+4% | 234 | 33% | 0.89% | -0.8% |
| >=+4% | 137 | 31% | 0.10% | -2.7% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 441 | 41% | 2.62% | 2.9% |
| 45-60% | 1292 | 35% | 0.97% | 0.1% |
| 60-75% | 1759 | 40% | 2.14% | 0.8% |
| >=75% | 916 | 41% | 2.98% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3270 | 39% | 2.20% | 1.50% | +0.69% | 52% |
| plus:accumulation | 2522 | 39% | 2.14% | 1.85% | +0.29% | 54% |
| flags:macd_divergence | 1852 | 39% | 2.64% | 1.57% | +1.07% | 52% |
| flags:overheat | 1592 | 34% | 0.40% | 2.93% | -2.53% | 64% |
| plus:power_gap | 1181 | 36% | 1.46% | 2.22% | -0.77% | 59% |
| flags:deep_base | 868 | 29% | -0.22% | 2.57% | -2.78% | 70% |
| flags:stop_inside_noise | 853 | 28% | -0.36% | 2.59% | -2.95% | 71% |
| flags:volume_spike_5x | 266 | 35% | 0.78% | 2.10% | -1.32% | 58% |
| plus:tight_base | 257 | 42% | 2.80% | 1.97% | +0.83% | 44% |
| flags:heavy_selling_day | 193 | 37% | 1.23% | 2.05% | -0.82% | 50% |
| flags:macd_fading | 76 | 37% | 3.15% | 2.00% | +1.15% | 57% |
| flags:distribution | 15 (small) | 47% | 2.41% | 2.02% | +0.39% | 47% |

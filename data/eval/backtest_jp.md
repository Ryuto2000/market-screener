# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-09 to 2026-10-16, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2596

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2585 | 0.0% | -0.2% | 47% | -5.3% | 5.4% |
| 10d | 2577 | 0.3% | 0.1% | 50% | -7.0% | 7.7% |
| 20d | 2557 | 1.3% | 0.6% | 53% | -8.8% | 11.9% |
| 40d | 2527 | 2.9% | 2.0% | 57% | -11.3% | 17.6% |
| 60d | 2466 | 4.5% | 3.1% | 59% | -14.1% | 23.6% |

First within 60 sessions: -8% stop 1200, +16% 723, neither 673. Median MFE 11.5%, median MAE -7.6%, MAE p10 -21.2%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2596 | 43% | 15.4% | -6.2% | 3.07% | 1.87 | 40.0/16.0 | 69% |
| close stop | 2596 | 43% | 17.8% | -7.0% | 3.77% | 1.96 | 46.0/21.0 | 70% |

Add-on: intraday: added in 38%, add lot mean 1.61% of the initial position; close: added in 40%, add lot mean 2.08% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 138 | 28% | -2.91% | -0.9% |
| 2023 | 737 | 44% | 3.13% | 1.1% |
| 2024 | 576 | 35% | -0.08% | 1.1% |
| 2025 | 710 | 53% | 8.65% | 2.0% |
| 2026 | 435 | 38% | -0.08% | 1.4% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 520 | 40% | 1.67% | 1.6% |
| uptrend | 2038 | 44% | 3.43% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1057 | 43% | 2.34% | 1.2% |
| >=5 | 1539 | 42% | 3.57% | 1.3% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 738 | 44% | 3.45% | 1.2% |
| 80-89 | 696 | 43% | 3.51% | 1.9% |
| 90-99 | 146 | 38% | 2.14% | 0.7% |
| <70 | 1016 | 42% | 2.61% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 52 | 40% | 4.05% | 1.0% |
| -2..-1% | 126 | 40% | 2.87% | 0.0% |
| -1..+1% | 2200 | 43% | 2.96% | 1.3% |
| +1..+2% | 196 | 44% | 4.51% | 2.6% |
| >=+2% | 22 | 45% | -0.38% | -2.6% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 86 | 35% | 0.31% | 1.2% |
| -2..0% | 969 | 45% | 3.92% | 1.9% |
| 0..+2% | 1416 | 42% | 2.63% | 0.9% |
| +2..+4% | 92 | 41% | 3.46% | 0.6% |
| >=+4% | 33 | 45% | 2.98% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 235 | 46% | 4.82% | 2.4% |
| 45-60% | 762 | 39% | 2.64% | 1.5% |
| 60-75% | 1105 | 42% | 2.03% | 0.7% |
| >=75% | 494 | 48% | 5.21% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1963 | 43% | 3.44% | 1.92% | +1.52% | 45% |
| flags:macd_divergence | 1275 | 43% | 3.76% | 2.40% | +1.37% | 46% |
| plus:accumulation | 1257 | 44% | 3.16% | 2.98% | +0.18% | 46% |
| plus:power_gap | 449 | 41% | 2.93% | 3.09% | -0.16% | 48% |
| plus:tight_base | 244 | 43% | 3.17% | 3.06% | +0.12% | 44% |
| flags:heavy_selling_day | 119 | 42% | 1.94% | 3.12% | -1.18% | 42% |
| flags:volume_spike_5x | 92 | 43% | 4.64% | 3.01% | +1.63% | 47% |
| flags:macd_fading | 28 | 32% | -0.42% | 3.10% | -3.52% | 61% |
| flags:distribution | 11 (small) | 45% | 3.96% | 3.06% | +0.89% | 45% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2596 | 43% / 43% | 3.07% | 3.77% | 1.3% | -3.2% / 3.8% / -0.8% / 10.7% / 0.7% |
| (b) within 3% of the 3-month high, next open | 8591 | 44% / 45% | 3.32% | 4.05% | 1.4% | -1.2% / 4.0% / -1.4% / 11.6% / 0.6% |
| (b) same, buy-stop above the high within 5 sessions | 4937 | 42% / 44% | 3.15% | 3.90% | 1.2% | -3.1% / 2.9% / -1.4% / 12.3% / 0.6% |
| (c) pullback re-entry, next open | 4459 | 46% / 47% | 3.55% | 4.29% | 1.8% | -1.4% / 3.8% / -2.0% / 11.7% / 1.0% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4396

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4377 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4363 | 0.3% | -0.2% | 49% | -9.3% | 9.5% |
| 20d | 4326 | 0.9% | 0.1% | 50% | -13.1% | 14.1% |
| 40d | 4269 | 2.4% | 1.0% | 53% | -16.1% | 21.2% |
| 60d | 4168 | 4.1% | 2.1% | 55% | -19.9% | 29.2% |

First within 60 sessions: -8% stop 2335, +16% 1247, neither 814. Median MFE 13.0%, median MAE -9.5%, MAE p10 -28.0%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4396 | 39% | 15.5% | -6.5% | 2.09% | 1.53 | 31.0/11.0 | 72% |
| close stop | 4396 | 40% | 18.8% | -7.6% | 2.92% | 1.63 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.23% of the initial position; close: added in 40%, add lot mean 1.76% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 213 | 26% | -3.15% | -1.5% |
| 2023 | 1134 | 40% | 2.25% | 0.4% |
| 2024 | 929 | 33% | -0.65% | 0.2% |
| 2025 | 1122 | 49% | 7.55% | 2.2% |
| 2026 | 998 | 35% | -0.58% | 1.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 850 | 38% | 1.00% | 0.7% |
| uptrend | 3486 | 39% | 2.34% | 0.9% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1756 | 39% | 1.84% | 0.9% |
| >=5 | 2640 | 39% | 2.25% | 0.9% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 909 | 43% | 3.16% | 1.1% |
| 80-89 | 1139 | 41% | 2.72% | 1.7% |
| 90-99 | 1221 | 33% | 0.44% | 0.0% |
| <70 | 1127 | 41% | 2.36% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 92 | 36% | 2.79% | -0.1% |
| -2..-1% | 227 | 37% | 1.38% | -0.3% |
| -1..+1% | 3700 | 39% | 1.99% | 0.9% |
| +1..+2% | 324 | 44% | 3.73% | 2.2% |
| >=+2% | 52 | 46% | 0.86% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 242 | 38% | 0.84% | 0.6% |
| -2..0% | 1542 | 41% | 2.83% | 1.8% |
| 0..+2% | 2243 | 39% | 1.95% | 0.7% |
| +2..+4% | 232 | 33% | 0.91% | -0.8% |
| >=+4% | 137 | 31% | 0.21% | -2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 394 | 43% | 3.37% | 3.0% |
| 45-60% | 1312 | 35% | 0.97% | 0.4% |
| 60-75% | 1776 | 41% | 2.16% | 0.8% |
| >=75% | 914 | 41% | 2.99% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3266 | 39% | 2.26% | 1.59% | +0.67% | 52% |
| plus:accumulation | 2520 | 39% | 2.20% | 1.94% | +0.25% | 54% |
| flags:macd_divergence | 1844 | 39% | 2.72% | 1.63% | +1.08% | 52% |
| flags:overheat | 1595 | 34% | 0.44% | 3.02% | -2.58% | 63% |
| plus:power_gap | 1172 | 36% | 1.57% | 2.28% | -0.71% | 59% |
| flags:deep_base | 868 | 29% | -0.19% | 2.65% | -2.84% | 70% |
| flags:stop_inside_noise | 856 | 28% | -0.39% | 2.69% | -3.07% | 71% |
| flags:volume_spike_5x | 263 | 36% | 1.10% | 2.15% | -1.05% | 58% |
| plus:tight_base | 257 | 43% | 2.93% | 2.04% | +0.89% | 44% |
| flags:heavy_selling_day | 191 | 38% | 1.29% | 2.12% | -0.83% | 51% |
| flags:macd_fading | 76 | 39% | 3.51% | 2.06% | +1.44% | 55% |
| flags:distribution | 13 (small) | 46% | 2.81% | 2.09% | +0.72% | 54% |

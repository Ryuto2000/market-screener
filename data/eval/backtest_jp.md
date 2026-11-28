# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-10-21 to 2026-11-25, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2615

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2608 | 0.0% | -0.2% | 47% | -5.3% | 5.5% |
| 10d | 2593 | 0.4% | 0.1% | 51% | -7.1% | 7.9% |
| 20d | 2554 | 1.2% | 0.6% | 53% | -9.1% | 11.9% |
| 40d | 2524 | 2.7% | 2.0% | 57% | -11.8% | 17.8% |
| 60d | 2484 | 4.4% | 3.0% | 58% | -14.4% | 23.6% |

First within 60 sessions: -8% stop 1212, +16% 729, neither 674. Median MFE 11.5%, median MAE -7.7%, MAE p10 -21.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2615 | 43% | 15.4% | -6.2% | 3.06% | 1.87 | 40.0/16.0 | 69% |
| close stop | 2615 | 43% | 17.7% | -7.0% | 3.72% | 1.94 | 46.0/21.0 | 70% |

Add-on: intraday: added in 39%, add lot mean 1.58% of the initial position; close: added in 40%, add lot mean 2.02% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 79 | 30% | -2.51% | -1.4% |
| 2023 | 740 | 44% | 3.11% | 1.1% |
| 2024 | 580 | 36% | -0.04% | 1.1% |
| 2025 | 711 | 53% | 8.65% | 1.9% |
| 2026 | 505 | 36% | -0.45% | 0.6% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 39 | 38% | 2.59% | 0.2% |
| mixed | 531 | 41% | 1.94% | 1.9% |
| uptrend | 2045 | 43% | 3.36% | 1.0% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1063 | 43% | 2.26% | 1.2% |
| >=5 | 1552 | 43% | 3.60% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 739 | 44% | 3.50% | 1.3% |
| 80-89 | 695 | 43% | 3.49% | 1.6% |
| 90-99 | 151 | 40% | 2.19% | 0.1% |
| <70 | 1030 | 42% | 2.58% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 69 | 41% | 3.11% | 1.0% |
| -2..-1% | 123 | 39% | 2.50% | 0.1% |
| -1..+1% | 2195 | 43% | 3.01% | 1.2% |
| +1..+2% | 204 | 44% | 4.34% | 2.5% |
| >=+2% | 24 | 46% | -0.44% | -2.7% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 92 | 36% | 0.34% | 1.1% |
| -2..0% | 975 | 45% | 3.84% | 1.8% |
| 0..+2% | 1418 | 42% | 2.69% | 0.8% |
| +2..+4% | 96 | 41% | 3.23% | 0.6% |
| >=+4% | 34 | 44% | 2.87% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 282 | 47% | 4.39% | 2.6% |
| 45-60% | 740 | 39% | 2.71% | 1.2% |
| 60-75% | 1097 | 42% | 1.99% | 0.7% |
| >=75% | 496 | 48% | 5.17% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1968 | 43% | 3.43% | 1.92% | +1.51% | 45% |
| flags:macd_divergence | 1280 | 43% | 3.77% | 2.37% | +1.40% | 46% |
| plus:accumulation | 1255 | 44% | 3.18% | 2.95% | +0.23% | 46% |
| plus:power_gap | 462 | 41% | 2.81% | 3.11% | -0.30% | 48% |
| plus:tight_base | 245 | 42% | 3.04% | 3.06% | -0.02% | 45% |
| flags:heavy_selling_day | 122 | 42% | 1.98% | 3.11% | -1.13% | 39% |
| flags:volume_spike_5x | 93 | 43% | 4.33% | 3.01% | +1.32% | 47% |
| flags:macd_fading | 27 | 26% | -1.24% | 3.10% | -4.34% | 67% |
| flags:distribution | 13 (small) | 54% | 3.85% | 3.05% | +0.80% | 38% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2615 | 43% / 43% | 3.06% | 3.72% | 1.2% | -2.8% / 3.8% / -0.7% / 10.6% / 0.1% |
| (b) within 3% of the 3-month high, next open | 8643 | 44% / 45% | 3.28% | 3.99% | 1.3% | -0.1% / 4.0% / -1.4% / 11.6% / -0.1% |
| (b) same, buy-stop above the high within 5 sessions | 4963 | 42% / 44% | 3.13% | 3.87% | 1.2% | -2.7% / 2.9% / -1.3% / 12.3% / 0.0% |
| (c) pullback re-entry, next open | 4481 | 46% / 47% | 3.53% | 4.26% | 1.8% | -0.7% / 3.8% / -2.0% / 11.7% / 0.4% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4410

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4402 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4383 | 0.3% | -0.1% | 49% | -9.4% | 9.6% |
| 20d | 4338 | 0.8% | 0.0% | 50% | -13.6% | 14.2% |
| 40d | 4285 | 2.2% | 0.9% | 53% | -16.8% | 21.3% |
| 60d | 4211 | 3.9% | 1.8% | 54% | -20.0% | 29.1% |

First within 60 sessions: -8% stop 2346, +16% 1255, neither 809. Median MFE 13.0%, median MAE -9.7%, MAE p10 -28.7%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4410 | 39% | 15.5% | -6.5% | 2.09% | 1.53 | 32.0/11.0 | 72% |
| close stop | 4410 | 40% | 18.8% | -7.6% | 2.90% | 1.63 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.21% of the initial position; close: added in 40%, add lot mean 1.73% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 131 | 27% | -2.84% | -1.2% |
| 2023 | 1137 | 40% | 2.24% | 0.4% |
| 2024 | 934 | 33% | -0.63% | 0.2% |
| 2025 | 1122 | 49% | 7.55% | 2.2% |
| 2026 | 1086 | 34% | -0.78% | 0.4% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 61 | 41% | 2.68% | 2.5% |
| mixed | 858 | 40% | 1.26% | 1.0% |
| uptrend | 3491 | 39% | 2.28% | 0.7% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1764 | 39% | 1.79% | 0.9% |
| >=5 | 2646 | 39% | 2.29% | 0.7% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 910 | 43% | 3.16% | 1.2% |
| 80-89 | 1134 | 41% | 2.76% | 1.6% |
| 90-99 | 1225 | 33% | 0.44% | -0.3% |
| <70 | 1141 | 41% | 2.34% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 107 | 36% | 2.43% | -0.3% |
| -2..-1% | 223 | 36% | 1.13% | -0.8% |
| -1..+1% | 3694 | 39% | 2.02% | 0.8% |
| +1..+2% | 332 | 43% | 3.61% | 2.1% |
| >=+2% | 53 | 47% | 0.95% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 249 | 37% | 0.76% | -0.5% |
| -2..0% | 1542 | 41% | 2.80% | 1.7% |
| 0..+2% | 2246 | 39% | 1.99% | 0.7% |
| +2..+4% | 235 | 33% | 0.89% | -0.9% |
| >=+4% | 138 | 30% | 0.09% | -2.7% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 453 | 43% | 3.07% | 3.0% |
| 45-60% | 1283 | 35% | 1.00% | -0.0% |
| 60-75% | 1758 | 40% | 2.17% | 0.8% |
| >=75% | 916 | 41% | 2.98% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3269 | 40% | 2.27% | 1.59% | +0.68% | 52% |
| plus:accumulation | 2511 | 39% | 2.21% | 1.93% | +0.28% | 54% |
| flags:macd_divergence | 1847 | 39% | 2.73% | 1.63% | +1.11% | 52% |
| flags:overheat | 1587 | 34% | 0.43% | 3.02% | -2.59% | 63% |
| plus:power_gap | 1185 | 36% | 1.50% | 2.31% | -0.81% | 59% |
| flags:deep_base | 866 | 29% | -0.20% | 2.65% | -2.85% | 70% |
| flags:stop_inside_noise | 850 | 28% | -0.34% | 2.67% | -3.00% | 71% |
| flags:volume_spike_5x | 264 | 35% | 0.75% | 2.17% | -1.43% | 59% |
| plus:tight_base | 258 | 42% | 2.80% | 2.05% | +0.76% | 45% |
| flags:heavy_selling_day | 194 | 38% | 1.37% | 2.12% | -0.75% | 49% |
| flags:macd_fading | 77 | 36% | 3.11% | 2.07% | +1.04% | 56% |
| flags:distribution | 15 (small) | 53% | 2.87% | 2.09% | +0.78% | 47% |

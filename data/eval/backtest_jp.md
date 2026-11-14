# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-10-07 to 2026-11-12, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2614

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2605 | 0.0% | -0.2% | 47% | -5.3% | 5.6% |
| 10d | 2575 | 0.4% | 0.1% | 51% | -7.0% | 7.9% |
| 20d | 2565 | 1.1% | 0.5% | 53% | -9.1% | 11.9% |
| 40d | 2527 | 2.9% | 2.0% | 57% | -11.5% | 17.7% |
| 60d | 2496 | 4.4% | 3.0% | 58% | -14.3% | 23.7% |

First within 60 sessions: -8% stop 1212, +16% 728, neither 674. Median MFE 11.5%, median MAE -7.7%, MAE p10 -21.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2614 | 43% | 15.3% | -6.2% | 3.05% | 1.87 | 40.0/16.0 | 69% |
| close stop | 2614 | 44% | 17.6% | -7.0% | 3.71% | 1.94 | 46.0/21.0 | 70% |

Add-on: intraday: added in 38%, add lot mean 1.59% of the initial position; close: added in 40%, add lot mean 2.03% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 100 | 31% | -2.58% | -1.2% |
| 2023 | 740 | 44% | 3.11% | 1.1% |
| 2024 | 580 | 36% | -0.04% | 1.1% |
| 2025 | 711 | 53% | 8.63% | 1.9% |
| 2026 | 483 | 37% | -0.37% | 0.5% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 532 | 42% | 1.87% | 1.7% |
| uptrend | 2044 | 43% | 3.36% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1059 | 43% | 2.29% | 1.3% |
| >=5 | 1555 | 43% | 3.56% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 738 | 45% | 3.50% | 1.2% |
| 80-89 | 699 | 42% | 3.42% | 1.6% |
| 90-99 | 151 | 39% | 2.15% | 0.1% |
| <70 | 1026 | 42% | 2.61% | 0.9% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 69 | 41% | 3.02% | 1.0% |
| -2..-1% | 124 | 40% | 2.57% | 0.3% |
| -1..+1% | 2195 | 43% | 3.00% | 1.1% |
| +1..+2% | 202 | 45% | 4.38% | 2.5% |
| >=+2% | 24 | 42% | -0.69% | -2.7% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 90 | 38% | 0.50% | 1.3% |
| -2..0% | 976 | 44% | 3.79% | 1.8% |
| 0..+2% | 1420 | 42% | 2.68% | 0.7% |
| +2..+4% | 94 | 41% | 3.46% | 0.6% |
| >=+4% | 34 | 44% | 2.81% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 283 | 47% | 4.18% | 2.2% |
| 45-60% | 738 | 39% | 2.74% | 1.2% |
| 60-75% | 1097 | 42% | 2.01% | 0.7% |
| >=75% | 496 | 48% | 5.17% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1973 | 43% | 3.41% | 1.93% | +1.49% | 46% |
| flags:macd_divergence | 1283 | 43% | 3.72% | 2.40% | +1.32% | 46% |
| plus:accumulation | 1260 | 44% | 3.18% | 2.93% | +0.24% | 46% |
| plus:power_gap | 460 | 42% | 2.91% | 3.08% | -0.17% | 47% |
| plus:tight_base | 244 | 42% | 3.06% | 3.05% | +0.01% | 45% |
| flags:heavy_selling_day | 123 | 42% | 1.94% | 3.10% | -1.16% | 40% |
| flags:volume_spike_5x | 93 | 44% | 4.40% | 3.00% | +1.40% | 47% |
| flags:macd_fading | 28 | 29% | -1.20% | 3.10% | -4.30% | 64% |
| flags:distribution | 13 (small) | 54% | 3.86% | 3.05% | +0.82% | 38% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2614 | 43% / 44% | 3.05% | 3.71% | 1.1% | -2.9% / 3.8% / -0.7% / 10.6% / 0.2% |
| (b) within 3% of the 3-month high, next open | 8622 | 44% / 45% | 3.31% | 4.00% | 1.3% | -0.3% / 4.0% / -1.4% / 11.6% / -0.0% |
| (b) same, buy-stop above the high within 5 sessions | 4953 | 42% / 44% | 3.13% | 3.86% | 1.2% | -2.9% / 2.9% / -1.3% / 12.3% / 0.1% |
| (c) pullback re-entry, next open | 4449 | 46% / 47% | 3.55% | 4.28% | 1.8% | -1.1% / 3.8% / -2.0% / 11.7% / 0.4% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4410

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4400 | -0.0% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4365 | 0.3% | -0.1% | 49% | -9.4% | 9.5% |
| 20d | 4345 | 0.8% | 0.0% | 50% | -13.5% | 14.1% |
| 40d | 4278 | 2.4% | 1.0% | 53% | -16.2% | 21.2% |
| 60d | 4216 | 3.9% | 1.7% | 54% | -20.0% | 29.0% |

First within 60 sessions: -8% stop 2345, +16% 1252, neither 813. Median MFE 13.0%, median MAE -9.7%, MAE p10 -28.5%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4410 | 39% | 15.4% | -6.5% | 2.09% | 1.53 | 32.0/11.0 | 72% |
| close stop | 4410 | 40% | 18.8% | -7.7% | 2.89% | 1.63 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.23% of the initial position; close: added in 40%, add lot mean 1.74% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 157 | 28% | -2.97% | -1.7% |
| 2023 | 1137 | 40% | 2.24% | 0.4% |
| 2024 | 934 | 33% | -0.63% | 0.2% |
| 2025 | 1123 | 49% | 7.54% | 2.2% |
| 2026 | 1059 | 34% | -0.71% | 0.5% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 859 | 40% | 1.21% | 0.9% |
| uptrend | 3491 | 39% | 2.29% | 0.7% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1757 | 39% | 1.82% | 0.9% |
| >=5 | 2653 | 39% | 2.27% | 0.7% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 909 | 43% | 3.16% | 1.2% |
| 80-89 | 1139 | 40% | 2.72% | 1.6% |
| 90-99 | 1225 | 33% | 0.45% | -0.3% |
| <70 | 1137 | 42% | 2.37% | 0.7% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 107 | 37% | 2.49% | -0.3% |
| -2..-1% | 224 | 36% | 1.17% | -0.4% |
| -1..+1% | 3695 | 39% | 2.02% | 0.7% |
| +1..+2% | 330 | 43% | 3.58% | 2.0% |
| >=+2% | 53 | 45% | 0.84% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 247 | 38% | 0.87% | -0.1% |
| -2..0% | 1543 | 41% | 2.76% | 1.7% |
| 0..+2% | 2249 | 40% | 2.00% | 0.6% |
| +2..+4% | 233 | 33% | 0.97% | -0.8% |
| >=+4% | 138 | 30% | 0.08% | -2.5% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 455 | 44% | 2.92% | 2.7% |
| 45-60% | 1280 | 35% | 1.02% | 0.0% |
| 60-75% | 1759 | 40% | 2.20% | 0.8% |
| >=75% | 916 | 41% | 2.98% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3275 | 40% | 2.26% | 1.60% | +0.66% | 52% |
| plus:accumulation | 2520 | 39% | 2.20% | 1.94% | +0.27% | 54% |
| flags:macd_divergence | 1850 | 39% | 2.70% | 1.65% | +1.05% | 52% |
| flags:overheat | 1592 | 34% | 0.43% | 3.03% | -2.59% | 64% |
| plus:power_gap | 1183 | 36% | 1.54% | 2.29% | -0.75% | 58% |
| flags:deep_base | 867 | 29% | -0.17% | 2.64% | -2.82% | 70% |
| flags:stop_inside_noise | 851 | 28% | -0.32% | 2.67% | -2.99% | 70% |
| flags:volume_spike_5x | 266 | 36% | 0.86% | 2.17% | -1.30% | 58% |
| plus:tight_base | 257 | 42% | 2.82% | 2.05% | +0.77% | 44% |
| flags:heavy_selling_day | 195 | 39% | 1.35% | 2.12% | -0.77% | 49% |
| flags:macd_fading | 76 | 38% | 3.22% | 2.07% | +1.15% | 57% |
| flags:distribution | 15 (small) | 53% | 2.88% | 2.09% | +0.80% | 47% |

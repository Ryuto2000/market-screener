# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-10-17 to 2026-11-19, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2617

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2607 | 0.0% | -0.2% | 47% | -5.3% | 5.5% |
| 10d | 2593 | 0.4% | 0.1% | 51% | -7.0% | 7.9% |
| 20d | 2559 | 1.1% | 0.5% | 53% | -9.2% | 11.9% |
| 40d | 2525 | 2.8% | 2.0% | 57% | -11.6% | 17.8% |
| 60d | 2490 | 4.3% | 3.0% | 58% | -14.3% | 23.6% |

First within 60 sessions: -8% stop 1215, +16% 727, neither 675. Median MFE 11.5%, median MAE -7.7%, MAE p10 -21.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2617 | 43% | 15.3% | -6.2% | 3.02% | 1.86 | 40.0/16.0 | 70% |
| close stop | 2617 | 43% | 17.6% | -7.0% | 3.67% | 1.93 | 46.0/21.0 | 70% |

Add-on: intraday: added in 38%, add lot mean 1.58% of the initial position; close: added in 40%, add lot mean 2.01% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 88 | 31% | -2.56% | -2.1% |
| 2023 | 740 | 44% | 3.11% | 1.1% |
| 2024 | 580 | 36% | -0.04% | 1.1% |
| 2025 | 711 | 53% | 8.63% | 1.9% |
| 2026 | 498 | 37% | -0.57% | 0.5% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 534 | 41% | 1.76% | 1.7% |
| uptrend | 2045 | 43% | 3.35% | 1.0% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1061 | 43% | 2.28% | 1.3% |
| >=5 | 1556 | 43% | 3.53% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 738 | 44% | 3.45% | 1.2% |
| 80-89 | 699 | 43% | 3.45% | 1.6% |
| 90-99 | 150 | 38% | 2.08% | -0.0% |
| <70 | 1030 | 42% | 2.56% | 0.9% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 69 | 41% | 2.81% | 1.0% |
| -2..-1% | 123 | 39% | 2.48% | 0.1% |
| -1..+1% | 2199 | 43% | 2.98% | 1.1% |
| +1..+2% | 202 | 43% | 4.27% | 2.4% |
| >=+2% | 24 | 46% | -0.59% | -2.7% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 92 | 36% | 0.25% | 1.1% |
| -2..0% | 979 | 44% | 3.76% | 1.7% |
| 0..+2% | 1417 | 42% | 2.68% | 0.8% |
| +2..+4% | 95 | 41% | 3.33% | 0.6% |
| >=+4% | 34 | 44% | 2.73% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 286 | 47% | 3.99% | 2.1% |
| 45-60% | 738 | 39% | 2.74% | 1.2% |
| 60-75% | 1097 | 42% | 1.99% | 0.7% |
| >=75% | 496 | 48% | 5.17% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1974 | 43% | 3.38% | 1.92% | +1.46% | 46% |
| flags:macd_divergence | 1283 | 43% | 3.71% | 2.35% | +1.36% | 46% |
| plus:accumulation | 1260 | 44% | 3.15% | 2.90% | +0.25% | 46% |
| plus:power_gap | 461 | 41% | 2.82% | 3.06% | -0.24% | 48% |
| plus:tight_base | 245 | 42% | 3.02% | 3.02% | -0.00% | 45% |
| flags:heavy_selling_day | 123 | 42% | 1.93% | 3.07% | -1.15% | 39% |
| flags:volume_spike_5x | 93 | 43% | 4.30% | 2.97% | +1.33% | 47% |
| flags:macd_fading | 28 | 29% | -1.19% | 3.07% | -4.26% | 64% |
| flags:distribution | 13 (small) | 54% | 3.87% | 3.02% | +0.85% | 38% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2617 | 43% / 43% | 3.02% | 3.67% | 1.1% | -2.8% / 3.8% / -0.7% / 10.6% / -0.1% |
| (b) within 3% of the 3-month high, next open | 8641 | 44% / 45% | 3.27% | 3.96% | 1.3% | -0.2% / 4.0% / -1.4% / 11.6% / -0.2% |
| (b) same, buy-stop above the high within 5 sessions | 4971 | 42% / 43% | 3.10% | 3.82% | 1.2% | -2.8% / 2.9% / -1.3% / 12.3% / -0.1% |
| (c) pullback re-entry, next open | 4465 | 46% / 47% | 3.53% | 4.25% | 1.8% | -0.9% / 3.8% / -2.0% / 11.7% / 0.2% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4415

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4403 | -0.1% | -0.3% | 46% | -7.3% | 7.0% |
| 10d | 4386 | 0.3% | -0.1% | 49% | -9.4% | 9.6% |
| 20d | 4343 | 0.8% | 0.0% | 50% | -13.6% | 14.2% |
| 40d | 4279 | 2.3% | 1.0% | 53% | -16.5% | 21.2% |
| 60d | 4215 | 3.9% | 1.7% | 54% | -20.0% | 28.9% |

First within 60 sessions: -8% stop 2347, +16% 1252, neither 816. Median MFE 13.0%, median MAE -9.7%, MAE p10 -28.6%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4415 | 39% | 15.4% | -6.5% | 2.06% | 1.52 | 32.0/11.0 | 72% |
| close stop | 4415 | 40% | 18.8% | -7.7% | 2.86% | 1.62 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.21% of the initial position; close: added in 40%, add lot mean 1.73% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 143 | 27% | -2.96% | -2.1% |
| 2023 | 1137 | 40% | 2.24% | 0.4% |
| 2024 | 934 | 33% | -0.63% | 0.2% |
| 2025 | 1123 | 49% | 7.54% | 2.2% |
| 2026 | 1078 | 34% | -0.84% | 0.4% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 863 | 39% | 1.10% | 0.9% |
| uptrend | 3492 | 39% | 2.29% | 0.7% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1760 | 39% | 1.80% | 0.9% |
| >=5 | 2655 | 39% | 2.24% | 0.6% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 909 | 43% | 3.12% | 1.2% |
| 80-89 | 1139 | 41% | 2.73% | 1.6% |
| 90-99 | 1226 | 32% | 0.41% | -0.3% |
| <70 | 1141 | 41% | 2.33% | 0.7% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 107 | 36% | 2.24% | -0.3% |
| -2..-1% | 223 | 36% | 1.12% | -0.8% |
| -1..+1% | 3701 | 39% | 2.01% | 0.7% |
| +1..+2% | 330 | 42% | 3.51% | 2.0% |
| >=+2% | 53 | 47% | 0.89% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 249 | 37% | 0.72% | -0.1% |
| -2..0% | 1545 | 40% | 2.75% | 1.7% |
| 0..+2% | 2249 | 39% | 1.98% | 0.6% |
| +2..+4% | 234 | 33% | 0.93% | -0.9% |
| >=+4% | 138 | 30% | 0.06% | -2.7% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 459 | 43% | 2.74% | 2.7% |
| 45-60% | 1281 | 35% | 1.01% | -0.0% |
| 60-75% | 1759 | 40% | 2.18% | 0.8% |
| >=75% | 916 | 41% | 2.98% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3277 | 39% | 2.23% | 1.59% | +0.64% | 52% |
| plus:accumulation | 2519 | 39% | 2.19% | 1.90% | +0.29% | 54% |
| flags:macd_divergence | 1851 | 39% | 2.69% | 1.61% | +1.07% | 52% |
| flags:overheat | 1591 | 34% | 0.42% | 2.99% | -2.56% | 63% |
| plus:power_gap | 1187 | 36% | 1.49% | 2.27% | -0.78% | 58% |
| flags:deep_base | 868 | 29% | -0.19% | 2.61% | -2.80% | 70% |
| flags:stop_inside_noise | 852 | 28% | -0.34% | 2.64% | -2.98% | 70% |
| flags:volume_spike_5x | 266 | 35% | 0.79% | 2.15% | -1.36% | 58% |
| plus:tight_base | 258 | 42% | 2.78% | 2.02% | +0.76% | 45% |
| flags:heavy_selling_day | 195 | 38% | 1.31% | 2.10% | -0.78% | 49% |
| flags:macd_fading | 77 | 38% | 3.11% | 2.04% | +1.07% | 56% |
| flags:distribution | 15 (small) | 53% | 2.89% | 2.06% | +0.82% | 47% |

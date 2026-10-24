# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-15 to 2026-10-22, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 2588

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2585 | 0.0% | -0.2% | 47% | -5.3% | 5.4% |
| 10d | 2570 | 0.3% | 0.1% | 51% | -6.9% | 7.8% |
| 20d | 2555 | 1.2% | 0.6% | 53% | -8.8% | 11.9% |
| 40d | 2522 | 2.9% | 2.0% | 57% | -11.3% | 17.6% |
| 60d | 2461 | 4.5% | 3.1% | 59% | -14.1% | 23.6% |

First within 60 sessions: -8% stop 1208, +16% 724, neither 656. Median MFE 11.6%, median MAE -7.7%, MAE p10 -21.5%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2588 | 43% | 15.5% | -6.2% | 3.06% | 1.86 | 40.0/16.0 | 69% |
| close stop | 2588 | 43% | 17.9% | -7.0% | 3.74% | 1.94 | 46.0/21.0 | 70% |

Add-on: intraday: added in 39%, add lot mean 1.61% of the initial position; close: added in 40%, add lot mean 2.06% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 127 | 28% | -2.88% | -0.7% |
| 2023 | 737 | 44% | 3.13% | 1.1% |
| 2024 | 576 | 35% | -0.08% | 1.1% |
| 2025 | 710 | 53% | 8.65% | 2.0% |
| 2026 | 438 | 37% | -0.25% | 1.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 2.87% | 0.1% |
| mixed | 512 | 40% | 1.72% | 1.7% |
| uptrend | 2038 | 43% | 3.40% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1056 | 43% | 2.30% | 1.3% |
| >=5 | 1532 | 42% | 3.58% | 1.2% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 733 | 44% | 3.50% | 1.2% |
| 80-89 | 695 | 43% | 3.46% | 1.8% |
| 90-99 | 146 | 38% | 2.14% | 0.5% |
| <70 | 1014 | 42% | 2.60% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 49 | 39% | 4.38% | 1.0% |
| -2..-1% | 126 | 40% | 2.62% | 0.0% |
| -1..+1% | 2194 | 43% | 2.96% | 1.2% |
| +1..+2% | 197 | 45% | 4.51% | 2.6% |
| >=+2% | 22 | 45% | -0.38% | -2.6% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 84 | 35% | 0.46% | 1.4% |
| -2..0% | 967 | 45% | 3.87% | 1.9% |
| 0..+2% | 1412 | 42% | 2.64% | 0.8% |
| +2..+4% | 92 | 41% | 3.46% | 0.6% |
| >=+4% | 33 | 45% | 2.98% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 238 | 47% | 4.87% | 2.4% |
| 45-60% | 766 | 39% | 2.55% | 1.3% |
| 60-75% | 1090 | 42% | 2.05% | 0.8% |
| >=75% | 494 | 48% | 5.21% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1953 | 43% | 3.45% | 1.87% | +1.58% | 46% |
| flags:macd_divergence | 1272 | 43% | 3.77% | 2.37% | +1.40% | 46% |
| plus:accumulation | 1253 | 44% | 3.18% | 2.95% | +0.22% | 46% |
| plus:power_gap | 450 | 41% | 2.90% | 3.09% | -0.19% | 48% |
| plus:tight_base | 243 | 43% | 3.21% | 3.05% | +0.17% | 44% |
| flags:heavy_selling_day | 120 | 42% | 1.93% | 3.12% | -1.18% | 42% |
| flags:volume_spike_5x | 92 | 43% | 4.51% | 3.01% | +1.51% | 48% |
| flags:macd_fading | 28 | 32% | -0.45% | 3.10% | -3.55% | 61% |
| flags:distribution | 11 (small) | 45% | 3.96% | 3.06% | +0.90% | 45% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2588 | 43% / 43% | 3.06% | 3.74% | 1.2% | -3.3% / 3.8% / -0.8% / 10.7% / 0.4% |
| (b) within 3% of the 3-month high, next open | 8592 | 44% / 45% | 3.30% | 4.01% | 1.4% | -0.8% / 4.0% / -1.4% / 11.6% / 0.2% |
| (b) same, buy-stop above the high within 5 sessions | 4928 | 42% / 43% | 3.14% | 3.87% | 1.2% | -2.8% / 2.9% / -1.4% / 12.3% / 0.2% |
| (c) pullback re-entry, next open | 4473 | 46% / 46% | 3.49% | 4.22% | 1.8% | -1.4% / 3.8% / -2.0% / 11.7% / 0.5% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4383

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4377 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4351 | 0.4% | -0.1% | 49% | -9.3% | 9.5% |
| 20d | 4324 | 0.9% | 0.1% | 50% | -13.2% | 14.2% |
| 40d | 4260 | 2.5% | 1.1% | 53% | -16.1% | 21.2% |
| 60d | 4159 | 4.1% | 2.1% | 55% | -19.9% | 29.2% |

First within 60 sessions: -8% stop 2340, +16% 1249, neither 794. Median MFE 13.0%, median MAE -9.6%, MAE p10 -28.1%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4383 | 39% | 15.5% | -6.5% | 2.09% | 1.53 | 31.0/11.0 | 72% |
| close stop | 4383 | 40% | 19.0% | -7.7% | 2.90% | 1.63 | 37.0/14.0 | 73% |

Add-on: intraday: added in 37%, add lot mean 1.23% of the initial position; close: added in 40%, add lot mean 1.76% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 194 | 26% | -3.02% | -1.1% |
| 2023 | 1134 | 40% | 2.25% | 0.4% |
| 2024 | 929 | 33% | -0.65% | 0.2% |
| 2025 | 1122 | 49% | 7.55% | 2.2% |
| 2026 | 1004 | 34% | -0.67% | 1.0% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 2.86% | 2.5% |
| mixed | 837 | 39% | 1.06% | 0.9% |
| uptrend | 3486 | 39% | 2.33% | 0.9% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1755 | 39% | 1.82% | 0.9% |
| >=5 | 2628 | 39% | 2.27% | 0.9% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 905 | 43% | 3.18% | 1.2% |
| 80-89 | 1137 | 41% | 2.72% | 1.7% |
| 90-99 | 1216 | 33% | 0.46% | 0.1% |
| <70 | 1125 | 41% | 2.35% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 86 | 35% | 3.12% | -0.3% |
| -2..-1% | 227 | 36% | 1.16% | -0.3% |
| -1..+1% | 3692 | 39% | 2.01% | 0.9% |
| +1..+2% | 325 | 43% | 3.66% | 2.2% |
| >=+2% | 52 | 46% | 0.86% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 238 | 37% | 0.92% | 0.6% |
| -2..0% | 1539 | 41% | 2.81% | 1.8% |
| 0..+2% | 2237 | 39% | 1.96% | 0.7% |
| +2..+4% | 232 | 33% | 0.91% | -0.8% |
| >=+4% | 137 | 31% | 0.24% | -2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 400 | 44% | 3.32% | 3.0% |
| 45-60% | 1318 | 35% | 0.92% | 0.3% |
| 60-75% | 1751 | 40% | 2.22% | 0.9% |
| >=75% | 914 | 41% | 2.99% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3252 | 39% | 2.28% | 1.57% | +0.71% | 52% |
| plus:accumulation | 2512 | 39% | 2.20% | 1.94% | +0.26% | 54% |
| flags:macd_divergence | 1841 | 39% | 2.73% | 1.63% | +1.11% | 52% |
| flags:overheat | 1590 | 34% | 0.47% | 3.02% | -2.54% | 63% |
| plus:power_gap | 1172 | 36% | 1.53% | 2.30% | -0.76% | 59% |
| flags:deep_base | 864 | 29% | -0.14% | 2.64% | -2.79% | 70% |
| flags:stop_inside_noise | 850 | 28% | -0.34% | 2.68% | -3.01% | 70% |
| flags:volume_spike_5x | 264 | 36% | 0.91% | 2.17% | -1.26% | 59% |
| plus:tight_base | 256 | 43% | 2.96% | 2.04% | +0.92% | 44% |
| flags:heavy_selling_day | 192 | 39% | 1.29% | 2.13% | -0.84% | 51% |
| flags:macd_fading | 76 | 39% | 3.50% | 2.07% | +1.43% | 55% |
| flags:distribution | 13 (small) | 46% | 2.81% | 2.09% | +0.72% | 54% |

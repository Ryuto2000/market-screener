# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-09-15 to 2026-10-29, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 252

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 252 | 0.4% | 0.5% | 56% | -6.7% | 7.6% |
| 10d | 252 | 1.0% | 0.8% | 55% | -8.5% | 10.1% |
| 20d | 252 | 2.5% | 2.2% | 60% | -11.3% | 18.2% |
| 40d | 252 | 6.8% | 4.3% | 62% | -15.3% | 25.0% |
| 60d | 251 | 10.1% | 5.3% | 61% | -19.0% | 38.8% |

First within 60 sessions: -8% stop 120, +16% 93, neither 39. Median MFE 17.4%, median MAE -8.4%, MAE p10 -28.3%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 252 | 44% | 18.1% | -6.1% | 4.67% | 2.38 | 32.0/13.5 | 70% |
| close stop | 252 | 45% | 23.8% | -7.7% | 6.45% | 2.53 | 38.0/17.0 | 71% |

Add-on: intraday: added in 46%, add lot mean 1.74% of the initial position; close: added in 50%, add lot mean 2.58% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2023 | 69 | 42% | 3.32% | -0.3% |
| 2024 | 154 | 49% | 6.11% | 3.8% |
| 2025 | 10 (small) | 30% | 6.28% | -2.8% |
| 2026 | 19 (small) | 26% | -2.99% | 4.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| uptrend | 252 | 44% | 4.67% | 2.5% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 252 | 44% | 4.67% | 2.5% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 90-99 | 252 | 44% | 4.67% | 2.5% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| -2..-1% | 8 (small) | 38% | 0.16% | -0.4% |
| -1..+1% | 238 | 44% | 4.65% | 2.4% |
| +1..+2% | 4 (small) | 75% | 17.58% | 14.6% |
| >=+2% | 2 (small) | 50% | -1.18% | -0.8% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 24 | 38% | -2.87% | 0.1% |
| -2..0% | 103 | 48% | 7.22% | 2.0% |
| 0..+2% | 99 | 43% | 3.18% | 2.5% |
| +2..+4% | 14 (small) | 29% | 7.98% | 3.3% |
| >=+4% | 12 (small) | 58% | 6.19% | 9.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 7 (small) | 57% | 12.79% | -1.2% |
| 45-60% | 51 | 35% | -1.07% | -0.2% |
| 60-75% | 126 | 44% | 5.14% | 4.2% |
| >=75% | 68 | 51% | 7.24% | 1.7% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 180 | 44% | 4.79% | 4.36% | +0.43% | 46% |
| plus:accumulation | 156 | 46% | 3.93% | 5.86% | -1.93% | 46% |
| flags:overheat | 139 | 39% | 4.24% | 5.19% | -0.94% | 51% |
| flags:macd_divergence | 102 | 54% | 7.26% | 2.90% | +4.35% | 38% |
| plus:power_gap | 81 | 38% | 0.77% | 6.51% | -5.74% | 51% |
| flags:deep_base | 73 | 48% | 5.86% | 4.18% | +1.68% | 53% |
| flags:stop_inside_noise | 53 | 38% | 2.82% | 5.16% | -2.34% | 64% |
| flags:heavy_selling_day | 13 (small) | 38% | 0.05% | 4.92% | -4.87% | 46% |
| plus:tight_base | 10 (small) | 30% | -0.72% | 4.89% | -5.61% | 60% |
| flags:macd_fading | 4 (small) | 25% | -1.39% | 4.76% | -6.15% | 50% |
| flags:volume_spike_5x | 4 (small) | 50% | -1.46% | 4.76% | -6.23% | 75% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 252 | 44% / 45% | 4.67% | 6.45% | 2.5% | 3.7% / 8.3% / 15.7% / -3.6% |
| (b) within 3% of the 3-month high, next open | 679 | 39% / 41% | 2.04% | 2.27% | 0.1% | 6.4% / 0.8% / 1.0% / 0.5% |
| (b) same, buy-stop above the high within 5 sessions | 418 | 38% / 40% | 2.27% | 2.86% | 0.6% | 6.2% / 1.3% / 5.5% / 1.5% |
| (c) pullback re-entry, next open | 298 | 45% / 45% | 3.35% | 3.38% | 1.7% | 5.6% / 2.6% / 4.1% / -6.8% |


# Backtest US: all breakout signals (before the market rules)


Signals: 2658

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2653 | 0.1% | 0.1% | 51% | -5.1% | 5.2% |
| 10d | 2645 | 0.5% | 0.2% | 52% | -6.7% | 7.7% |
| 20d | 2634 | 1.0% | 0.5% | 54% | -9.3% | 11.3% |
| 40d | 2623 | 2.1% | 1.1% | 54% | -12.7% | 16.7% |
| 60d | 2605 | 4.0% | 1.9% | 57% | -15.8% | 22.4% |

First within 60 sessions: -8% stop 1307, +16% 588, neither 763. Median MFE 10.1%, median MAE -8.2%, MAE p10 -21.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2658 | 40% | 12.2% | -6.1% | 1.23% | 1.34 | 37.5/18.0 | 75% |
| close stop | 2658 | 41% | 14.0% | -7.0% | 1.68% | 1.41 | 45.0/23.0 | 75% |

Add-on: intraday: added in 35%, add lot mean 0.54% of the initial position; close: added in 37%, add lot mean 0.61% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 84 | 26% | -3.70% | -0.1% |
| 2023 | 587 | 44% | 2.46% | 0.5% |
| 2024 | 907 | 44% | 2.36% | 2.0% |
| 2025 | 544 | 38% | 1.60% | 1.1% |
| 2026 | 536 | 33% | -1.61% | 0.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 90 | 31% | -0.96% | 1.6% |
| mixed | 551 | 37% | 0.69% | 0.4% |
| uptrend | 2017 | 41% | 1.48% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 923 | 41% | 1.54% | 0.9% |
| >=5 | 1735 | 40% | 1.07% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 493 | 42% | 0.80% | 0.4% |
| 80-89 | 784 | 40% | 0.86% | 0.7% |
| 90-99 | 966 | 40% | 2.57% | 2.0% |
| <70 | 415 | 39% | -0.67% | 0.3% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 25 | 44% | 0.30% | 3.6% |
| -2..-1% | 112 | 29% | -2.27% | -0.5% |
| -1..+1% | 2441 | 40% | 1.40% | 1.1% |
| +1..+2% | 74 | 42% | 1.43% | 1.4% |
| >=+2% | 6 (small) | 33% | -1.23% | 3.4% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 121 | 40% | 2.29% | 1.7% |
| -2..0% | 1101 | 41% | 1.48% | 0.9% |
| 0..+2% | 1304 | 40% | 0.86% | 0.8% |
| +2..+4% | 87 | 33% | 0.79% | 3.7% |
| >=+4% | 45 | 33% | 4.06% | 2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 329 | 43% | 2.00% | 0.9% |
| 45-60% | 736 | 39% | 1.76% | 0.6% |
| 60-75% | 1133 | 39% | 0.57% | 1.5% |
| >=75% | 460 | 42% | 1.47% | 0.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1900 | 40% | 0.97% | 1.89% | -0.93% | 49% |
| plus:accumulation | 1204 | 40% | 1.42% | 1.08% | +0.35% | 49% |
| flags:macd_divergence | 1192 | 41% | 1.35% | 1.14% | +0.21% | 51% |
| flags:overheat | 552 | 38% | 1.77% | 1.09% | +0.68% | 54% |
| plus:power_gap | 503 | 39% | 2.29% | 0.99% | +1.30% | 51% |
| flags:deep_base | 295 | 42% | 4.26% | 0.85% | +3.41% | 56% |
| flags:stop_inside_noise | 237 | 34% | 2.21% | 1.14% | +1.08% | 67% |
| plus:tight_base | 209 | 40% | 0.61% | 1.29% | -0.67% | 47% |
| flags:heavy_selling_day | 118 | 41% | 1.13% | 1.24% | -0.10% | 52% |
| flags:macd_fading | 50 | 60% | 9.17% | 1.08% | +8.09% | 30% |
| flags:volume_spike_5x | 40 | 62% | 8.03% | 1.13% | +6.90% | 42% |
| flags:distribution | 18 (small) | 33% | -1.48% | 1.25% | -2.73% | 61% |

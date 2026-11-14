# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-10-04 to 2026-11-11, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 252

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 252 | 0.4% | 0.5% | 57% | -6.6% | 7.6% |
| 10d | 252 | 1.0% | 0.7% | 54% | -8.3% | 10.1% |
| 20d | 252 | 2.6% | 2.3% | 60% | -11.1% | 18.2% |
| 40d | 252 | 7.1% | 4.7% | 63% | -15.0% | 25.0% |
| 60d | 251 | 10.5% | 5.6% | 62% | -18.8% | 38.8% |

First within 60 sessions: -8% stop 118, +16% 95, neither 39. Median MFE 17.6%, median MAE -8.0%, MAE p10 -27.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 252 | 45% | 18.0% | -6.1% | 4.82% | 2.45 | 32.0/14.0 | 69% |
| close stop | 252 | 46% | 23.5% | -7.5% | 6.65% | 2.62 | 39.0/17.0 | 71% |

Add-on: intraday: added in 47%, add lot mean 1.70% of the initial position; close: added in 51%, add lot mean 2.52% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2023 | 69 | 43% | 3.56% | 0.1% |
| 2024 | 154 | 49% | 6.25% | 3.9% |
| 2025 | 10 (small) | 30% | 6.28% | -2.8% |
| 2026 | 19 (small) | 26% | -2.99% | 4.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| uptrend | 252 | 45% | 4.82% | 2.6% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 252 | 45% | 4.82% | 2.6% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 90-99 | 252 | 45% | 4.82% | 2.6% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| -2..-1% | 7 (small) | 43% | 1.56% | 0.1% |
| -1..+1% | 239 | 45% | 4.75% | 2.5% |
| +1..+2% | 4 (small) | 75% | 17.58% | 14.6% |
| >=+2% | 2 (small) | 50% | -1.18% | -0.8% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 22 | 41% | -2.33% | 1.0% |
| -2..0% | 105 | 49% | 7.29% | 2.1% |
| 0..+2% | 99 | 43% | 3.18% | 2.5% |
| +2..+4% | 14 (small) | 29% | 7.98% | 3.3% |
| >=+4% | 12 (small) | 58% | 6.19% | 9.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 7 (small) | 57% | 12.79% | -1.2% |
| 45-60% | 51 | 35% | -1.07% | -0.2% |
| 60-75% | 127 | 44% | 5.20% | 4.2% |
| >=75% | 67 | 54% | 7.74% | 2.1% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 180 | 45% | 5.00% | 4.36% | +0.64% | 44% |
| plus:accumulation | 154 | 47% | 4.10% | 5.95% | -1.86% | 45% |
| flags:overheat | 138 | 39% | 4.33% | 5.41% | -1.08% | 51% |
| flags:macd_divergence | 104 | 55% | 7.32% | 3.06% | +4.26% | 38% |
| plus:power_gap | 81 | 40% | 0.97% | 6.64% | -5.67% | 49% |
| flags:deep_base | 72 | 49% | 6.05% | 4.32% | +1.73% | 53% |
| flags:stop_inside_noise | 53 | 40% | 3.13% | 5.27% | -2.14% | 62% |
| flags:heavy_selling_day | 13 (small) | 38% | 0.05% | 5.08% | -5.03% | 46% |
| plus:tight_base | 10 (small) | 30% | -0.72% | 5.05% | -5.77% | 60% |
| flags:volume_spike_5x | 5 (small) | 60% | 0.48% | 4.91% | -4.42% | 60% |
| flags:macd_fading | 4 (small) | 25% | -1.39% | 4.92% | -6.31% | 50% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 252 | 45% / 46% | 4.82% | 6.65% | 2.6% | 3.9% / 8.6% / 15.7% / -3.6% |
| (b) within 3% of the 3-month high, next open | 678 | 39% / 41% | 2.09% | 2.32% | 0.2% | 6.4% / 0.9% / 1.0% / 0.5% |
| (b) same, buy-stop above the high within 5 sessions | 418 | 38% / 40% | 2.30% | 2.88% | 0.7% | 6.2% / 1.3% / 5.5% / 1.5% |
| (c) pullback re-entry, next open | 294 | 45% / 45% | 3.43% | 3.46% | 1.8% | 5.7% / 2.5% / 4.9% / -6.8% |


# Backtest US: all breakout signals (before the market rules)


Signals: 2702

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2698 | 0.1% | 0.1% | 51% | -5.1% | 5.2% |
| 10d | 2667 | 0.5% | 0.2% | 52% | -6.7% | 7.7% |
| 20d | 2645 | 1.0% | 0.6% | 54% | -9.3% | 11.3% |
| 40d | 2627 | 2.1% | 1.1% | 54% | -12.7% | 16.8% |
| 60d | 2615 | 4.0% | 2.0% | 57% | -15.8% | 22.4% |

First within 60 sessions: -8% stop 1317, +16% 591, neither 794. Median MFE 9.9%, median MAE -8.0%, MAE p10 -21.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2702 | 40% | 12.0% | -6.1% | 1.19% | 1.33 | 38.0/17.0 | 75% |
| close stop | 2702 | 42% | 13.7% | -7.0% | 1.62% | 1.40 | 45.0/23.0 | 76% |

Add-on: intraday: added in 34%, add lot mean 0.52% of the initial position; close: added in 37%, add lot mean 0.57% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 82 | 24% | -3.83% | -0.2% |
| 2023 | 587 | 44% | 2.53% | 0.6% |
| 2024 | 910 | 45% | 2.37% | 2.0% |
| 2025 | 544 | 38% | 1.60% | 1.1% |
| 2026 | 579 | 34% | -1.68% | -0.0% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 88 | 30% | -1.02% | 1.6% |
| mixed | 596 | 38% | 0.57% | 0.4% |
| uptrend | 2018 | 42% | 1.47% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 923 | 41% | 1.53% | 0.9% |
| >=5 | 1779 | 40% | 1.02% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 504 | 42% | 0.45% | 0.3% |
| 80-89 | 800 | 40% | 0.96% | 0.7% |
| 90-99 | 982 | 41% | 2.54% | 2.0% |
| <70 | 416 | 39% | -0.64% | 0.3% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 25 | 44% | 0.30% | 3.6% |
| -2..-1% | 111 | 29% | -2.21% | -0.6% |
| -1..+1% | 2484 | 41% | 1.35% | 1.1% |
| +1..+2% | 76 | 42% | 1.42% | 1.4% |
| >=+2% | 6 (small) | 33% | -1.23% | 3.4% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 122 | 42% | 2.36% | 1.8% |
| -2..0% | 1118 | 41% | 1.46% | 0.9% |
| 0..+2% | 1328 | 40% | 0.79% | 0.8% |
| +2..+4% | 88 | 34% | 0.81% | 3.6% |
| >=+4% | 46 | 33% | 3.80% | 2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 328 | 43% | 1.89% | 0.7% |
| 45-60% | 752 | 39% | 1.71% | 0.7% |
| 60-75% | 1164 | 39% | 0.53% | 1.5% |
| >=75% | 458 | 43% | 1.54% | 0.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1926 | 40% | 0.95% | 1.79% | -0.84% | 49% |
| plus:accumulation | 1211 | 40% | 1.40% | 1.03% | +0.37% | 48% |
| flags:macd_divergence | 1206 | 41% | 1.31% | 1.10% | +0.20% | 50% |
| flags:overheat | 556 | 38% | 1.67% | 1.07% | +0.60% | 54% |
| plus:power_gap | 512 | 39% | 2.17% | 0.96% | +1.21% | 50% |
| flags:deep_base | 295 | 42% | 4.12% | 0.84% | +3.28% | 57% |
| flags:stop_inside_noise | 239 | 33% | 1.99% | 1.12% | +0.87% | 68% |
| plus:tight_base | 209 | 40% | 0.61% | 1.24% | -0.63% | 47% |
| flags:heavy_selling_day | 121 | 42% | 1.17% | 1.19% | -0.02% | 51% |
| flags:macd_fading | 50 | 60% | 9.17% | 1.04% | +8.12% | 30% |
| flags:volume_spike_5x | 42 | 62% | 7.21% | 1.10% | +6.11% | 43% |
| flags:distribution | 22 | 32% | -1.90% | 1.22% | -3.12% | 55% |

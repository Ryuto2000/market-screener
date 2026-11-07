# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-10-04 to 2026-11-05, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)
- earnings: sold at the close before estimated results (volume spike in the reporting season) unless the stop is at entry +1% or higher

Signals: 253

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 253 | 0.4% | 0.5% | 57% | -6.7% | 7.5% |
| 10d | 253 | 0.9% | 0.6% | 54% | -8.5% | 10.1% |
| 20d | 253 | 2.5% | 2.3% | 60% | -11.2% | 18.2% |
| 40d | 253 | 6.9% | 4.5% | 63% | -15.1% | 25.0% |
| 60d | 252 | 10.3% | 5.6% | 62% | -19.0% | 38.6% |

First within 60 sessions: -8% stop 119, +16% 95, neither 39. Median MFE 17.5%, median MAE -8.1%, MAE p10 -28.3%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 253 | 45% | 18.0% | -6.1% | 4.77% | 2.43 | 32.0/14.0 | 69% |
| close stop | 253 | 45% | 23.5% | -7.5% | 6.59% | 2.60 | 39.0/17.0 | 71% |

Add-on: intraday: added in 47%, add lot mean 1.70% of the initial position; close: added in 51%, add lot mean 2.52% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2023 | 70 | 43% | 3.39% | -0.1% |
| 2024 | 154 | 49% | 6.25% | 3.9% |
| 2025 | 10 (small) | 30% | 6.28% | -2.8% |
| 2026 | 19 (small) | 26% | -2.99% | 4.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| uptrend | 253 | 45% | 4.77% | 2.5% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 253 | 45% | 4.77% | 2.5% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 90-99 | 253 | 45% | 4.77% | 2.5% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| -2..-1% | 7 (small) | 43% | 1.56% | 0.1% |
| -1..+1% | 240 | 45% | 4.70% | 2.4% |
| +1..+2% | 4 (small) | 75% | 17.58% | 14.6% |
| >=+2% | 2 (small) | 50% | -1.18% | -0.8% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 23 | 39% | -2.58% | 0.2% |
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
| >=75% | 68 | 53% | 7.51% | 1.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 181 | 45% | 4.93% | 4.36% | +0.57% | 45% |
| plus:accumulation | 155 | 46% | 4.02% | 5.95% | -1.94% | 46% |
| flags:overheat | 139 | 39% | 4.24% | 5.41% | -1.17% | 51% |
| flags:macd_divergence | 104 | 55% | 7.32% | 2.99% | +4.33% | 38% |
| plus:power_gap | 82 | 39% | 0.86% | 6.64% | -5.78% | 50% |
| flags:deep_base | 73 | 48% | 5.86% | 4.32% | +1.54% | 53% |
| flags:stop_inside_noise | 54 | 39% | 2.92% | 5.27% | -2.35% | 63% |
| flags:heavy_selling_day | 13 (small) | 38% | 0.05% | 5.02% | -4.98% | 46% |
| plus:tight_base | 10 (small) | 30% | -0.72% | 4.99% | -5.71% | 60% |
| flags:volume_spike_5x | 5 (small) | 60% | 0.48% | 4.85% | -4.37% | 60% |
| flags:macd_fading | 4 (small) | 25% | -1.39% | 4.87% | -6.26% | 50% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 253 | 45% / 45% | 4.77% | 6.59% | 2.5% | 3.7% / 8.6% / 15.7% / -3.6% |
| (b) within 3% of the 3-month high, next open | 678 | 39% / 41% | 2.07% | 2.29% | 0.2% | 6.4% / 0.8% / 1.0% / 0.5% |
| (b) same, buy-stop above the high within 5 sessions | 418 | 38% / 40% | 2.27% | 2.87% | 0.7% | 6.2% / 1.3% / 5.5% / 1.5% |
| (c) pullback re-entry, next open | 297 | 44% / 44% | 3.31% | 3.34% | 1.6% | 5.6% / 2.5% / 4.1% / -6.8% |


# Backtest US: all breakout signals (before the market rules)


Signals: 2703

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2673 | 0.1% | 0.1% | 51% | -5.1% | 5.2% |
| 10d | 2658 | 0.5% | 0.2% | 52% | -6.7% | 7.7% |
| 20d | 2641 | 1.0% | 0.6% | 54% | -9.3% | 11.3% |
| 40d | 2629 | 2.1% | 1.1% | 54% | -12.7% | 16.7% |
| 60d | 2613 | 4.0% | 2.0% | 57% | -15.8% | 22.4% |

First within 60 sessions: -8% stop 1320, +16% 592, neither 791. Median MFE 9.9%, median MAE -8.1%, MAE p10 -21.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2703 | 40% | 12.0% | -6.1% | 1.17% | 1.32 | 38.0/17.0 | 76% |
| close stop | 2703 | 41% | 13.8% | -7.0% | 1.59% | 1.39 | 45.0/23.0 | 76% |

Add-on: intraday: added in 34%, add lot mean 0.52% of the initial position; close: added in 37%, add lot mean 0.58% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 82 | 24% | -3.83% | -0.2% |
| 2023 | 589 | 44% | 2.49% | 0.5% |
| 2024 | 911 | 45% | 2.36% | 2.0% |
| 2025 | 544 | 38% | 1.60% | 1.1% |
| 2026 | 577 | 33% | -1.76% | -0.0% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 88 | 30% | -1.02% | 1.6% |
| mixed | 593 | 37% | 0.47% | 0.5% |
| uptrend | 2022 | 41% | 1.47% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 926 | 41% | 1.55% | 0.9% |
| >=5 | 1777 | 39% | 0.97% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 505 | 42% | 0.72% | 0.4% |
| 80-89 | 799 | 39% | 0.76% | 0.7% |
| 90-99 | 979 | 41% | 2.53% | 2.0% |
| <70 | 420 | 38% | -0.68% | 0.3% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 25 | 44% | 0.30% | 3.6% |
| -2..-1% | 111 | 28% | -2.29% | -0.6% |
| -1..+1% | 2485 | 41% | 1.33% | 1.1% |
| +1..+2% | 76 | 41% | 1.36% | 1.4% |
| >=+2% | 6 (small) | 33% | -1.23% | 3.4% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 123 | 41% | 2.27% | 1.7% |
| -2..0% | 1116 | 41% | 1.43% | 0.9% |
| 0..+2% | 1330 | 40% | 0.78% | 0.8% |
| +2..+4% | 88 | 33% | 0.75% | 3.7% |
| >=+4% | 46 | 33% | 3.80% | 2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 328 | 42% | 1.86% | 0.8% |
| 45-60% | 753 | 39% | 1.71% | 0.7% |
| 60-75% | 1156 | 39% | 0.48% | 1.5% |
| >=75% | 466 | 42% | 1.52% | 0.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1928 | 40% | 0.91% | 1.82% | -0.90% | 49% |
| plus:accumulation | 1215 | 40% | 1.39% | 1.00% | +0.39% | 48% |
| flags:macd_divergence | 1206 | 41% | 1.30% | 1.07% | +0.23% | 51% |
| flags:overheat | 557 | 38% | 1.63% | 1.05% | +0.58% | 54% |
| plus:power_gap | 514 | 39% | 2.17% | 0.94% | +1.24% | 50% |
| flags:deep_base | 296 | 42% | 4.08% | 0.81% | +3.27% | 57% |
| flags:stop_inside_noise | 241 | 34% | 2.09% | 1.08% | +1.01% | 68% |
| plus:tight_base | 209 | 40% | 0.59% | 1.22% | -0.62% | 47% |
| flags:heavy_selling_day | 121 | 40% | 1.01% | 1.18% | -0.17% | 51% |
| flags:macd_fading | 50 | 60% | 9.17% | 1.02% | +8.15% | 30% |
| flags:volume_spike_5x | 42 | 62% | 7.40% | 1.07% | +6.33% | 40% |
| flags:distribution | 21 | 29% | -1.53% | 1.19% | -2.73% | 52% |

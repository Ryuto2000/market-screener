# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-10-13 to 2026-11-25, entry at the next open after the signal day
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
| 60d | 252 | 10.4% | 5.6% | 62% | -18.8% | 38.6% |

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
| (b) within 3% of the 3-month high, next open | 676 | 39% / 41% | 2.12% | 2.35% | 0.2% | 6.5% / 0.9% / 1.0% / 0.5% |
| (b) same, buy-stop above the high within 5 sessions | 418 | 38% / 40% | 2.30% | 2.88% | 0.7% | 6.2% / 1.3% / 5.5% / 1.5% |
| (c) pullback re-entry, next open | 294 | 45% / 45% | 3.43% | 3.46% | 1.8% | 5.7% / 2.5% / 4.9% / -6.8% |


# Backtest US: all breakout signals (before the market rules)


Signals: 2703

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2699 | 0.1% | 0.1% | 51% | -5.1% | 5.2% |
| 10d | 2698 | 0.4% | 0.2% | 52% | -6.8% | 7.7% |
| 20d | 2654 | 1.0% | 0.5% | 54% | -9.3% | 11.3% |
| 40d | 2630 | 2.1% | 1.0% | 54% | -12.8% | 16.7% |
| 60d | 2617 | 4.0% | 1.9% | 57% | -15.8% | 22.4% |

First within 60 sessions: -8% stop 1330, +16% 591, neither 782. Median MFE 9.8%, median MAE -8.2%, MAE p10 -21.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2703 | 40% | 12.0% | -6.1% | 1.17% | 1.32 | 38.0/17.0 | 75% |
| close stop | 2703 | 41% | 13.8% | -7.0% | 1.60% | 1.39 | 45.0/23.0 | 76% |

Add-on: intraday: added in 34%, add lot mean 0.52% of the initial position; close: added in 37%, add lot mean 0.58% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 80 | 26% | -3.62% | -0.4% |
| 2023 | 587 | 44% | 2.53% | 0.6% |
| 2024 | 910 | 45% | 2.37% | 2.0% |
| 2025 | 543 | 38% | 1.60% | 1.1% |
| 2026 | 583 | 33% | -1.81% | -0.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 86 | 31% | -0.75% | 1.4% |
| mixed | 600 | 38% | 0.45% | 0.4% |
| uptrend | 2017 | 41% | 1.47% | 1.1% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 924 | 41% | 1.54% | 0.9% |
| >=5 | 1779 | 40% | 0.98% | 1.0% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 504 | 42% | 0.45% | 0.3% |
| 80-89 | 799 | 39% | 0.93% | 0.7% |
| 90-99 | 983 | 41% | 2.51% | 1.9% |
| <70 | 417 | 39% | -0.65% | 0.3% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 26 | 46% | 0.30% | 3.6% |
| -2..-1% | 107 | 29% | -2.10% | -0.6% |
| -1..+1% | 2486 | 41% | 1.32% | 1.0% |
| +1..+2% | 78 | 44% | 1.43% | 1.4% |
| >=+2% | 6 (small) | 33% | -1.23% | 3.4% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 124 | 41% | 2.17% | 1.7% |
| -2..0% | 1119 | 41% | 1.48% | 0.9% |
| 0..+2% | 1326 | 40% | 0.76% | 0.8% |
| +2..+4% | 88 | 33% | 0.72% | 3.6% |
| >=+4% | 46 | 33% | 3.80% | 2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 325 | 42% | 1.89% | 0.6% |
| 45-60% | 757 | 39% | 1.66% | 0.6% |
| 60-75% | 1157 | 39% | 0.48% | 1.5% |
| >=75% | 464 | 43% | 1.58% | 0.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1928 | 40% | 0.92% | 1.80% | -0.88% | 50% |
| plus:accumulation | 1210 | 40% | 1.37% | 1.01% | +0.35% | 49% |
| flags:macd_divergence | 1207 | 41% | 1.28% | 1.08% | +0.20% | 51% |
| flags:overheat | 558 | 38% | 1.62% | 1.05% | +0.56% | 55% |
| plus:power_gap | 511 | 39% | 2.13% | 0.95% | +1.19% | 51% |
| flags:deep_base | 297 | 42% | 4.04% | 0.82% | +3.22% | 57% |
| flags:stop_inside_noise | 240 | 34% | 2.00% | 1.09% | +0.91% | 68% |
| plus:tight_base | 209 | 40% | 0.61% | 1.22% | -0.61% | 47% |
| flags:heavy_selling_day | 121 | 41% | 1.06% | 1.18% | -0.11% | 52% |
| flags:macd_fading | 50 | 60% | 9.17% | 1.02% | +8.15% | 30% |
| flags:volume_spike_5x | 42 | 62% | 7.21% | 1.08% | +6.14% | 43% |
| flags:distribution | 22 | 32% | -2.21% | 1.20% | -3.41% | 64% |

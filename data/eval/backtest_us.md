# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-09-07 to 2026-10-15, entry at the next open after the signal day
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
| 40d | 251 | 6.7% | 4.3% | 62% | -15.3% | 25.0% |
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


Signals: 2649

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2642 | 0.1% | 0.1% | 51% | -5.1% | 5.1% |
| 10d | 2640 | 0.4% | 0.2% | 52% | -6.8% | 7.7% |
| 20d | 2633 | 1.0% | 0.5% | 54% | -9.3% | 11.3% |
| 40d | 2621 | 2.1% | 1.1% | 54% | -12.7% | 16.7% |
| 60d | 2588 | 4.1% | 2.1% | 57% | -15.8% | 22.5% |

First within 60 sessions: -8% stop 1311, +16% 586, neither 752. Median MFE 10.1%, median MAE -8.2%, MAE p10 -21.7%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2649 | 40% | 12.2% | -6.1% | 1.20% | 1.33 | 38.0/17.0 | 75% |
| close stop | 2649 | 41% | 14.0% | -7.0% | 1.64% | 1.40 | 45.0/23.0 | 76% |

Add-on: intraday: added in 35%, add lot mean 0.54% of the initial position; close: added in 37%, add lot mean 0.60% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 90 | 24% | -4.02% | -0.7% |
| 2023 | 587 | 44% | 2.46% | 0.5% |
| 2024 | 907 | 44% | 2.36% | 2.0% |
| 2025 | 544 | 38% | 1.60% | 1.1% |
| 2026 | 521 | 31% | -1.75% | 0.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 96 | 29% | -1.43% | 1.0% |
| mixed | 542 | 37% | 0.73% | 0.4% |
| uptrend | 2011 | 41% | 1.45% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 923 | 41% | 1.53% | 0.9% |
| >=5 | 1726 | 39% | 1.02% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 492 | 41% | 0.78% | 0.4% |
| 80-89 | 780 | 39% | 0.87% | 0.7% |
| 90-99 | 963 | 40% | 2.49% | 2.0% |
| <70 | 414 | 38% | -0.68% | 0.3% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 26 | 42% | -0.02% | 2.9% |
| -2..-1% | 108 | 28% | -2.37% | -0.5% |
| -1..+1% | 2435 | 40% | 1.37% | 1.1% |
| +1..+2% | 74 | 42% | 1.51% | 1.4% |
| >=+2% | 6 (small) | 33% | -1.23% | 3.4% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 122 | 40% | 2.20% | 1.6% |
| -2..0% | 1093 | 40% | 1.47% | 0.9% |
| 0..+2% | 1303 | 40% | 0.81% | 0.8% |
| +2..+4% | 86 | 33% | 0.77% | 3.7% |
| >=+4% | 45 | 33% | 4.06% | 2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 328 | 42% | 1.88% | 1.0% |
| 45-60% | 730 | 38% | 1.74% | 0.6% |
| 60-75% | 1131 | 39% | 0.54% | 1.5% |
| >=75% | 460 | 42% | 1.47% | 0.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1890 | 39% | 0.94% | 1.85% | -0.92% | 50% |
| plus:accumulation | 1205 | 40% | 1.39% | 1.04% | +0.35% | 49% |
| flags:macd_divergence | 1194 | 40% | 1.29% | 1.12% | +0.17% | 51% |
| flags:overheat | 548 | 38% | 1.72% | 1.06% | +0.65% | 55% |
| plus:power_gap | 501 | 39% | 2.29% | 0.94% | +1.35% | 51% |
| flags:deep_base | 295 | 42% | 4.10% | 0.84% | +3.26% | 57% |
| flags:stop_inside_noise | 238 | 34% | 2.09% | 1.11% | +0.98% | 68% |
| plus:tight_base | 209 | 40% | 0.59% | 1.25% | -0.66% | 47% |
| flags:heavy_selling_day | 117 | 40% | 1.11% | 1.20% | -0.10% | 52% |
| flags:macd_fading | 50 | 60% | 9.17% | 1.05% | +8.12% | 30% |
| flags:volume_spike_5x | 40 | 62% | 7.74% | 1.10% | +6.64% | 42% |
| flags:distribution | 18 (small) | 33% | -1.48% | 1.22% | -2.69% | 61% |

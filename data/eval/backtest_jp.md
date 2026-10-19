# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-09 to 2026-10-16, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)

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
| intraday stop | 2596 | 40% | 21.6% | -6.9% | 4.58% | 2.11 | 61.0/19.0 | 64% |
| close stop | 2596 | 41% | 25.3% | -8.1% | 5.54% | 2.16 | 71.0/25.0 | 63% |

Add-on: intraday: added in 53%, add lot mean 1.74% of the initial position; close: added in 56%, add lot mean 2.16% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 138 | 28% | -1.95% | -0.9% |
| 2023 | 737 | 42% | 4.84% | 1.1% |
| 2024 | 576 | 31% | -0.18% | 1.1% |
| 2025 | 710 | 51% | 12.23% | 2.0% |
| 2026 | 435 | 35% | 0.01% | 1.4% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 38 | 39% | 3.73% | 0.1% |
| mixed | 520 | 36% | 3.31% | 1.6% |
| uptrend | 2038 | 41% | 4.92% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1057 | 40% | 3.64% | 1.2% |
| >=5 | 1539 | 40% | 5.23% | 1.3% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 734 | 40% | 4.48% | 1.1% |
| 80-89 | 700 | 41% | 4.96% | 1.8% |
| 90-99 | 143 | 34% | 2.73% | 0.9% |
| <70 | 1019 | 41% | 4.65% | 1.0% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 52 | 33% | 3.27% | 1.0% |
| -2..-1% | 126 | 34% | 2.89% | 0.0% |
| -1..+1% | 2200 | 41% | 4.51% | 1.3% |
| +1..+2% | 196 | 43% | 7.53% | 2.6% |
| >=+2% | 22 | 32% | -1.83% | -2.6% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 86 | 31% | 0.96% | 1.2% |
| -2..0% | 969 | 43% | 5.69% | 1.9% |
| 0..+2% | 1416 | 39% | 4.10% | 0.9% |
| +2..+4% | 92 | 34% | 3.17% | 0.6% |
| >=+4% | 33 | 42% | 5.70% | 1.6% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 236 | 42% | 5.03% | 2.4% |
| 45-60% | 761 | 36% | 3.69% | 1.5% |
| 60-75% | 1105 | 39% | 3.10% | 0.7% |
| >=75% | 494 | 47% | 9.03% | 1.6% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1963 | 41% | 4.90% | 3.59% | +1.31% | 45% |
| flags:macd_divergence | 1275 | 41% | 5.11% | 4.06% | +1.06% | 46% |
| plus:accumulation | 1257 | 41% | 4.60% | 4.56% | +0.04% | 46% |
| plus:power_gap | 449 | 37% | 2.77% | 4.96% | -2.18% | 48% |
| plus:tight_base | 244 | 40% | 3.85% | 4.65% | -0.80% | 44% |
| flags:heavy_selling_day | 119 | 40% | 4.36% | 4.59% | -0.23% | 42% |
| flags:volume_spike_5x | 92 | 42% | 4.43% | 4.58% | -0.15% | 47% |
| flags:macd_fading | 28 | 32% | -0.68% | 4.64% | -5.31% | 61% |
| flags:distribution | 11 (small) | 36% | 2.50% | 4.59% | -2.09% | 45% |


## Entry types (signals passing the market rules)

| entry | n | win (stop/close) | expectancy stop | expectancy close | 20d mean | close-stop expectancy by year: 2022 / 2023 / 2024 / 2025 / 2026 |
|---|---|---|---|---|---|---|
| (a) breakout with volume, next open | 2596 | 40% / 41% | 4.58% | 5.54% | 1.3% | -2.1% / 5.9% / -1.5% / 15.4% / 0.6% |
| (b) within 3% of the 3-month high, next open | 8596 | 41% / 42% | -228287.02% | -228285.86% | 1.4% | 0.4% / -839701.9% / -2.0% / 16.8% / 0.9% |
| (b) same, buy-stop above the high within 5 sessions | 4941 | 39% / 41% | -198507.88% | -198506.72% | 1.2% | -1.8% / -748736.4% / -1.8% / 17.6% / 0.8% |
| (c) pullback re-entry, next open | 4461 | 43% / 44% | -220023.20% | -220021.98% | 1.8% | 0.7% / -764439.0% / -2.7% / 17.2% / 1.2% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4397

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4378 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4364 | 0.3% | -0.2% | 49% | -9.3% | 9.5% |
| 20d | 4327 | 0.9% | 0.1% | 50% | -13.1% | 14.1% |
| 40d | 4269 | 2.4% | 1.0% | 53% | -16.1% | 21.2% |
| 60d | 4168 | 4.1% | 2.1% | 55% | -19.9% | 29.2% |

First within 60 sessions: -8% stop 2336, +16% 1247, neither 814. Median MFE 13.0%, median MAE -9.5%, MAE p10 -28.0%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4397 | 37% | 20.7% | -7.0% | 3.25% | 1.73 | 45.0/12.0 | 68% |
| close stop | 4397 | 38% | 25.2% | -8.5% | 4.33% | 1.82 | 54.0/16.0 | 67% |

Add-on: intraday: added in 48%, add lot mean 1.39% of the initial position; close: added in 52%, add lot mean 1.88% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 213 | 26% | -2.60% | -1.5% |
| 2023 | 1134 | 39% | 3.60% | 0.4% |
| 2024 | 929 | 29% | -0.76% | 0.2% |
| 2025 | 1122 | 48% | 10.60% | 2.2% |
| 2026 | 999 | 33% | -0.43% | 1.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 4.46% | 2.5% |
| mixed | 850 | 35% | 1.99% | 0.7% |
| uptrend | 3487 | 38% | 3.54% | 0.9% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1757 | 37% | 2.81% | 0.9% |
| >=5 | 2640 | 37% | 3.54% | 0.9% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 907 | 40% | 4.33% | 1.1% |
| 80-89 | 1144 | 38% | 3.81% | 1.7% |
| 90-99 | 1216 | 31% | 0.84% | 0.1% |
| <70 | 1130 | 40% | 4.41% | 0.8% |

## by_benchmark_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 92 | 32% | 2.35% | -0.1% |
| -2..-1% | 228 | 33% | 1.44% | -0.3% |
| -1..+1% | 3700 | 37% | 3.16% | 0.9% |
| +1..+2% | 324 | 43% | 6.34% | 2.2% |
| >=+2% | 52 | 38% | -0.01% | 2.1% |

## by_stock_gap_at_entry

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <=-2% | 243 | 35% | 1.21% | 0.6% |
| -2..0% | 1542 | 40% | 4.28% | 1.8% |
| 0..+2% | 2243 | 37% | 3.17% | 0.7% |
| +2..+4% | 232 | 28% | 0.67% | -0.8% |
| >=+4% | 137 | 30% | 0.87% | -2.4% |

## by_breadth50

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <45% | 397 | 39% | 3.61% | 3.0% |
| 45-60% | 1309 | 32% | 1.59% | 0.4% |
| 60-75% | 1777 | 38% | 3.01% | 0.8% |
| >=75% | 914 | 41% | 5.93% | 0.9% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3266 | 38% | 3.42% | 2.75% | +0.67% | 52% |
| plus:accumulation | 2520 | 37% | 3.20% | 3.32% | -0.12% | 54% |
| flags:macd_divergence | 1844 | 37% | 3.81% | 2.84% | +0.97% | 52% |
| flags:overheat | 1596 | 33% | 1.11% | 4.47% | -3.36% | 63% |
| plus:power_gap | 1172 | 34% | 1.80% | 3.78% | -1.97% | 59% |
| flags:deep_base | 869 | 28% | 0.11% | 4.02% | -3.91% | 70% |
| flags:stop_inside_noise | 857 | 28% | -0.21% | 4.09% | -4.30% | 71% |
| flags:volume_spike_5x | 263 | 35% | 1.23% | 3.38% | -2.15% | 58% |
| plus:tight_base | 257 | 41% | 3.78% | 3.22% | +0.56% | 44% |
| flags:heavy_selling_day | 191 | 36% | 3.03% | 3.26% | -0.23% | 51% |
| flags:macd_fading | 76 | 39% | 5.01% | 3.22% | +1.79% | 55% |
| flags:distribution | 13 (small) | 38% | 1.58% | 3.25% | -1.68% | 54% |

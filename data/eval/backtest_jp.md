# Backtest JP: signals that pass the current rules (screener/rules.py)

- market: jp, signals from 2022-09-08 to 2026-10-15, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)

Signals: 2598

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 2586 | -0.0% | -0.2% | 47% | -5.3% | 5.4% |
| 10d | 2579 | 0.3% | 0.1% | 50% | -7.1% | 7.7% |
| 20d | 2561 | 1.2% | 0.6% | 53% | -8.8% | 11.8% |
| 40d | 2531 | 2.9% | 2.0% | 57% | -11.4% | 17.6% |
| 60d | 2469 | 4.5% | 3.1% | 59% | -14.1% | 23.6% |

First within 60 sessions: -8% stop 1199, +16% 723, neither 676. Median MFE 11.5%, median MAE -7.6%, MAE p10 -21.2%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 2598 | 40% | 21.8% | -6.9% | 4.58% | 2.11 | 61.0/19.0 | 64% |
| close stop | 2598 | 41% | 25.4% | -8.1% | 5.53% | 2.15 | 71.0/25.0 | 63% |

Add-on: intraday: added in 53%, add lot mean 1.75% of the initial position; close: added in 56%, add lot mean 2.16% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 143 | 29% | -1.72% | -1.0% |
| 2023 | 737 | 42% | 4.84% | 1.1% |
| 2024 | 576 | 31% | -0.18% | 1.1% |
| 2025 | 710 | 51% | 12.23% | 2.0% |
| 2026 | 432 | 34% | -0.01% | 1.3% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 37 | 41% | 4.05% | 0.1% |
| mixed | 526 | 36% | 3.28% | 1.5% |
| uptrend | 2035 | 41% | 4.93% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1057 | 40% | 3.63% | 1.2% |
| >=5 | 1541 | 40% | 5.23% | 1.3% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 734 | 40% | 4.57% | 1.2% |
| 80-89 | 699 | 40% | 4.85% | 1.8% |
| 90-99 | 144 | 34% | 2.66% | 0.8% |
| <70 | 1021 | 41% | 4.67% | 1.0% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1968 | 41% | 4.89% | 3.62% | +1.27% | 45% |
| flags:macd_divergence | 1278 | 41% | 5.08% | 4.09% | +0.99% | 46% |
| plus:accumulation | 1259 | 40% | 4.54% | 4.61% | -0.07% | 46% |
| plus:power_gap | 448 | 37% | 2.76% | 4.96% | -2.20% | 48% |
| plus:tight_base | 244 | 39% | 3.83% | 4.66% | -0.83% | 44% |
| flags:heavy_selling_day | 120 | 39% | 4.29% | 4.59% | -0.30% | 42% |
| flags:volume_spike_5x | 92 | 42% | 4.43% | 4.58% | -0.16% | 47% |
| flags:macd_fading | 28 | 32% | -0.63% | 4.64% | -5.27% | 61% |
| flags:distribution | 11 (small) | 36% | 2.50% | 4.59% | -2.09% | 45% |


# Backtest JP: all breakout signals (before the market rules)


Signals: 4401

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 4380 | -0.1% | -0.3% | 46% | -7.3% | 6.9% |
| 10d | 4369 | 0.3% | -0.2% | 49% | -9.3% | 9.5% |
| 20d | 4335 | 0.9% | 0.1% | 50% | -13.1% | 14.1% |
| 40d | 4275 | 2.4% | 1.0% | 53% | -16.1% | 21.2% |
| 60d | 4173 | 4.1% | 2.0% | 55% | -19.8% | 29.2% |

First within 60 sessions: -8% stop 2337, +16% 1248, neither 816. Median MFE 13.0%, median MAE -9.5%, MAE p10 -27.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 4401 | 37% | 20.7% | -7.0% | 3.25% | 1.73 | 45.0/12.0 | 68% |
| close stop | 4401 | 38% | 25.3% | -8.5% | 4.32% | 1.82 | 54.0/16.0 | 67% |

Add-on: intraday: added in 48%, add lot mean 1.40% of the initial position; close: added in 52%, add lot mean 1.89% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 221 | 27% | -2.43% | -1.5% |
| 2023 | 1134 | 39% | 3.60% | 0.4% |
| 2024 | 929 | 29% | -0.76% | 0.2% |
| 2025 | 1123 | 48% | 10.58% | 2.3% |
| 2026 | 994 | 33% | -0.43% | 1.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 42% | 4.46% | 2.5% |
| mixed | 858 | 35% | 1.97% | 0.7% |
| uptrend | 3483 | 38% | 3.55% | 0.9% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1758 | 37% | 2.81% | 0.9% |
| >=5 | 2643 | 37% | 3.55% | 0.9% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 907 | 40% | 4.41% | 1.1% |
| 80-89 | 1144 | 38% | 3.74% | 1.7% |
| 90-99 | 1218 | 31% | 0.82% | 0.1% |
| <70 | 1132 | 40% | 4.43% | 0.8% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3271 | 38% | 3.42% | 2.75% | +0.68% | 52% |
| plus:accumulation | 2521 | 37% | 3.17% | 3.36% | -0.18% | 54% |
| flags:macd_divergence | 1850 | 37% | 3.79% | 2.86% | +0.93% | 52% |
| flags:overheat | 1596 | 33% | 1.12% | 4.46% | -3.35% | 63% |
| plus:power_gap | 1171 | 34% | 1.79% | 3.78% | -2.00% | 59% |
| flags:deep_base | 869 | 28% | 0.12% | 4.02% | -3.90% | 70% |
| flags:stop_inside_noise | 857 | 28% | -0.20% | 4.08% | -4.29% | 71% |
| flags:volume_spike_5x | 262 | 35% | 1.20% | 3.38% | -2.17% | 58% |
| plus:tight_base | 257 | 40% | 3.76% | 3.22% | +0.54% | 44% |
| flags:heavy_selling_day | 192 | 36% | 2.99% | 3.26% | -0.27% | 52% |
| flags:macd_fading | 76 | 39% | 5.04% | 3.22% | +1.82% | 55% |
| flags:distribution | 13 (small) | 38% | 1.58% | 3.26% | -1.68% | 54% |

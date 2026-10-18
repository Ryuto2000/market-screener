# Backtest US: signals that pass the current rules (screener/rules.py)

- market: us, signals from 2022-09-07 to 2026-10-15, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)

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
| intraday stop | 252 | 42% | 21.7% | -6.7% | 5.26% | 2.36 | 44.0/14.0 | 66% |
| close stop | 252 | 42% | 28.0% | -8.4% | 7.03% | 2.45 | 50.0/19.0 | 67% |

Add-on: intraday: added in 55%, add lot mean 1.62% of the initial position; close: added in 60%, add lot mean 2.31% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2023 | 69 | 41% | 4.28% | -0.3% |
| 2024 | 154 | 45% | 6.65% | 3.8% |
| 2025 | 10 (small) | 30% | 6.28% | -2.8% |
| 2026 | 19 (small) | 26% | -2.99% | 4.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| uptrend | 252 | 42% | 5.26% | 2.5% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 252 | 42% | 5.26% | 2.5% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 90-99 | 252 | 42% | 5.26% | 2.5% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 180 | 42% | 5.06% | 5.76% | -0.70% | 46% |
| plus:accumulation | 156 | 43% | 4.25% | 6.90% | -2.66% | 46% |
| flags:overheat | 139 | 40% | 4.65% | 6.01% | -1.36% | 51% |
| flags:macd_divergence | 102 | 53% | 8.24% | 3.23% | +5.01% | 38% |
| plus:power_gap | 81 | 41% | 1.20% | 7.18% | -5.98% | 51% |
| flags:deep_base | 73 | 45% | 6.45% | 4.77% | +1.68% | 53% |
| flags:stop_inside_noise | 53 | 40% | 3.20% | 5.81% | -2.61% | 64% |
| flags:heavy_selling_day | 13 (small) | 46% | 0.16% | 5.54% | -5.38% | 46% |
| plus:tight_base | 10 (small) | 30% | 6.26% | 5.22% | +1.04% | 60% |
| flags:macd_fading | 4 (small) | 25% | -1.39% | 5.37% | -6.76% | 50% |
| flags:volume_spike_5x | 4 (small) | 50% | -1.46% | 5.37% | -6.83% | 75% |


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
| intraday stop | 2649 | 33% | 17.8% | -6.8% | 1.33% | 1.29 | 62.0/22.0 | 72% |
| close stop | 2649 | 34% | 20.9% | -8.1% | 1.93% | 1.37 | 74.0/28.0 | 70% |

Add-on: intraday: added in 47%, add lot mean 0.40% of the initial position; close: added in 52%, add lot mean 0.49% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 90 | 17% | -5.15% | -0.7% |
| 2023 | 587 | 38% | 3.72% | 0.5% |
| 2024 | 907 | 36% | 2.64% | 2.0% |
| 2025 | 544 | 32% | 0.91% | 1.1% |
| 2026 | 521 | 27% | -2.09% | 0.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 96 | 22% | -2.43% | 1.0% |
| mixed | 542 | 29% | 0.67% | 0.4% |
| uptrend | 2011 | 35% | 1.68% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 923 | 34% | 1.78% | 0.9% |
| >=5 | 1726 | 32% | 1.09% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 492 | 32% | 1.46% | 0.4% |
| 80-89 | 780 | 33% | 0.84% | 0.7% |
| 90-99 | 963 | 36% | 2.59% | 2.0% |
| <70 | 414 | 28% | -0.85% | 0.3% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1890 | 33% | 0.99% | 2.17% | -1.18% | 50% |
| plus:accumulation | 1205 | 34% | 1.58% | 1.12% | +0.46% | 49% |
| flags:macd_divergence | 1194 | 34% | 1.41% | 1.26% | +0.15% | 51% |
| flags:overheat | 548 | 34% | 1.93% | 1.17% | +0.76% | 55% |
| plus:power_gap | 501 | 38% | 2.65% | 1.02% | +1.63% | 51% |
| flags:deep_base | 295 | 39% | 4.18% | 0.97% | +3.21% | 57% |
| flags:stop_inside_noise | 238 | 34% | 2.31% | 1.23% | +1.08% | 68% |
| plus:tight_base | 209 | 28% | 0.75% | 1.38% | -0.62% | 47% |
| flags:heavy_selling_day | 117 | 35% | 0.85% | 1.35% | -0.50% | 52% |
| flags:macd_fading | 50 | 56% | 8.41% | 1.19% | +7.22% | 30% |
| flags:volume_spike_5x | 40 | 57% | 7.51% | 1.23% | +6.28% | 42% |
| flags:distribution | 18 (small) | 28% | -3.56% | 1.36% | -4.92% | 61% |

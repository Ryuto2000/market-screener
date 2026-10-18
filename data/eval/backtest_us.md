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
| intraday stop | 252 | 38% | 21.5% | -5.5% | 4.86% | 2.43 | 62.0/14.0 | 53% |
| close stop | 252 | 46% | 20.0% | -7.6% | 5.21% | 2.28 | 67.0/19.0 | 48% |

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2023 | 69 | 45% | 5.09% | -0.3% |
| 2024 | 154 | 38% | 5.24% | 3.8% |
| 2025 | 10 (small) | 30% | 10.38% | -2.8% |
| 2026 | 19 (small) | 21% | -1.89% | 4.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| uptrend | 252 | 38% | 4.86% | 2.5% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 252 | 38% | 4.86% | 2.5% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 90-99 | 252 | 38% | 4.86% | 2.5% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 180 | 39% | 5.44% | 3.43% | +2.01% | 46% |
| plus:accumulation | 156 | 38% | 4.83% | 4.92% | -0.09% | 46% |
| flags:overheat | 139 | 35% | 4.39% | 5.45% | -1.06% | 51% |
| flags:macd_divergence | 102 | 52% | 7.63% | 2.98% | +4.65% | 38% |
| plus:power_gap | 81 | 36% | 2.65% | 5.91% | -3.26% | 51% |
| flags:deep_base | 73 | 41% | 6.31% | 4.27% | +2.03% | 53% |
| flags:stop_inside_noise | 53 | 30% | 3.09% | 5.34% | -2.25% | 64% |
| flags:heavy_selling_day | 13 (small) | 46% | 3.15% | 4.96% | -1.80% | 46% |
| plus:tight_base | 10 (small) | 30% | 4.18% | 4.89% | -0.71% | 60% |
| flags:macd_fading | 4 (small) | 25% | 0.69% | 4.93% | -4.24% | 50% |
| flags:volume_spike_5x | 4 (small) | 25% | -1.34% | 4.96% | -6.30% | 75% |


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
| intraday stop | 2649 | 30% | 16.9% | -5.9% | 0.94% | 1.23 | 72.0/23.0 | 55% |
| close stop | 2649 | 39% | 15.2% | -7.6% | 1.36% | 1.30 | 80.0/28.0 | 51% |

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 90 | 14% | -3.89% | -0.7% |
| 2023 | 587 | 36% | 1.96% | 0.5% |
| 2024 | 907 | 33% | 2.19% | 2.0% |
| 2025 | 544 | 28% | 0.76% | 1.1% |
| 2026 | 521 | 22% | -1.39% | 0.1% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 96 | 17% | -2.57% | 1.0% |
| mixed | 542 | 28% | 0.02% | 0.4% |
| uptrend | 2011 | 31% | 1.35% | 1.2% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 923 | 32% | 1.67% | 0.9% |
| >=5 | 1726 | 29% | 0.54% | 1.1% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 492 | 30% | 0.54% | 0.4% |
| 80-89 | 780 | 31% | 0.41% | 0.7% |
| 90-99 | 963 | 31% | 2.25% | 2.0% |
| <70 | 414 | 26% | -0.65% | 0.3% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 1890 | 29% | 0.80% | 1.27% | -0.48% | 50% |
| plus:accumulation | 1205 | 30% | 1.25% | 0.67% | +0.59% | 49% |
| flags:macd_divergence | 1194 | 30% | 0.86% | 0.99% | -0.13% | 51% |
| flags:overheat | 548 | 30% | 1.72% | 0.73% | +0.99% | 55% |
| plus:power_gap | 501 | 33% | 2.37% | 0.60% | +1.78% | 51% |
| flags:deep_base | 295 | 35% | 4.01% | 0.55% | +3.46% | 57% |
| flags:stop_inside_noise | 238 | 27% | 2.42% | 0.79% | +1.63% | 68% |
| plus:tight_base | 209 | 28% | 0.94% | 0.93% | +0.00% | 47% |
| flags:heavy_selling_day | 117 | 32% | 0.68% | 0.95% | -0.26% | 52% |
| flags:macd_fading | 50 | 50% | 7.30% | 0.81% | +6.49% | 30% |
| flags:volume_spike_5x | 40 | 50% | 7.03% | 0.84% | +6.19% | 42% |
| flags:distribution | 18 (small) | 17% | -3.37% | 0.96% | -4.33% | 61% |

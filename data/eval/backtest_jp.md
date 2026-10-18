# Backtest JP

- market: jp, signals from 2022-09-08 to 2026-10-15, entry at the next open after the signal day
- rules not modelled: market cap, fundamentals, earnings dates, theme/crypto exclusions
- survivorship bias: today's listings only, so results lean optimistic
- 'intraday' = resting stop order; 'close' = stop checked on the close, sold at the next open (odd lots)

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
| intraday stop | 4401 | 34% | 19.1% | -6.2% | 2.38% | 1.58 | 62.0/13.0 | 53% |
| close stop | 4401 | 42% | 17.9% | -8.1% | 2.87% | 1.61 | 65.0/16.0 | 51% |

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2022 | 221 | 24% | -1.41% | -1.5% |
| 2023 | 1134 | 36% | 2.80% | 0.4% |
| 2024 | 929 | 25% | -0.55% | 0.2% |
| 2025 | 1123 | 46% | 7.35% | 2.3% |
| 2026 | 994 | 28% | -0.13% | 1.2% |

## by_regime

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| downtrend | 60 | 32% | 2.86% | 2.5% |
| mixed | 858 | 32% | 1.37% | 0.7% |
| uptrend | 3483 | 34% | 2.62% | 0.9% |

## by_distribution_days

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| <5 | 1758 | 34% | 2.10% | 0.9% |
| >=5 | 2643 | 34% | 2.57% | 0.9% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 907 | 38% | 3.16% | 1.1% |
| 80-89 | 1144 | 34% | 2.92% | 1.7% |
| 90-99 | 1218 | 25% | 0.42% | 0.1% |
| <70 | 1132 | 39% | 3.32% | 0.8% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:above_upper_band | 3271 | 34% | 2.53% | 1.95% | +0.58% | 52% |
| plus:accumulation | 2521 | 33% | 2.28% | 2.51% | -0.23% | 54% |
| flags:macd_divergence | 1850 | 35% | 2.69% | 2.15% | +0.54% | 52% |
| flags:overheat | 1596 | 28% | 0.93% | 3.21% | -2.28% | 63% |
| plus:power_gap | 1171 | 28% | 1.17% | 2.82% | -1.65% | 59% |
| flags:deep_base | 869 | 23% | -0.13% | 3.00% | -3.13% | 70% |
| flags:stop_inside_noise | 857 | 23% | -0.04% | 2.96% | -3.00% | 71% |
| flags:volume_spike_5x | 262 | 30% | 0.98% | 2.47% | -1.49% | 58% |
| plus:tight_base | 257 | 40% | 3.05% | 2.34% | +0.71% | 44% |
| flags:heavy_selling_day | 192 | 31% | 2.38% | 2.38% | -0.00% | 52% |
| flags:macd_fading | 76 | 38% | 2.78% | 2.37% | +0.41% | 55% |
| flags:distribution | 13 (small) | 31% | 2.38% | 2.38% | -0.00% | 54% |

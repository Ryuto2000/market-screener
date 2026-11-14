# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-11-13
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 753

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 593 | -0.9% | -0.8% | 38% | -5.5% | 4.9% |
| 10d | 393 | -2.0% | -1.9% | 32% | -9.0% | 6.0% |
| 20d | 1 | 2.8% | 2.8% | 100% | 2.8% | 2.8% |

First within 60 sessions: -8% stop 181, +16% 9, neither 563. Median MFE 2.8%, median MAE -3.9%, MAE p10 -11.7%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 753 | 52% | 3.3% | -3.8% | -0.08% | 0.96 | 5.0/5.0 | 48% |
| close stop | 753 | 53% | 3.3% | -3.8% | -0.02% | 0.99 | 5.0/5.0 | 47% |

Add-on: intraday: added in 5%, add lot mean -0.19% of the initial position; close: added in 5%, add lot mean -0.06% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 753 | 52% | -0.08% | 2.8% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 178 | 62% | 0.80% | None |
| 80-89 | 191 | 50% | -0.93% | None |
| 90-99 | 31 | 42% | -1.88% | None |
| <70 | 352 | 50% | 0.10% | None |
| unknown | 1 (small) | 100% | 0.36% | 2.8% |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 262 | 53% | -0.04% | -0.10% | +0.06% | 25% |
| plus:accumulation | 243 | 41% | -0.68% | 0.21% | -0.89% | 29% |
| flags:above_upper_band | 152 | 59% | 0.36% | -0.19% | +0.55% | 18% |
| flags:macd_fading | 124 | 53% | -0.56% | 0.02% | -0.57% | 27% |
| plus:tight_base | 58 | 24% | -1.10% | 0.01% | -1.11% | 19% |
| flags:heavy_selling_day | 38 | 63% | 1.27% | -0.15% | +1.42% | 11% |
| flags:distribution | 20 | 85% | 2.86% | -0.16% | +3.02% | 5% |
| flags:macd_dead_cross | 13 (small) | 54% | -0.90% | -0.06% | -0.84% | 23% |
| flags:volume_spike_5x | 9 (small) | 44% | -2.89% | -0.04% | -2.85% | 44% |
| flags:wide_stop | 1 (small) | 0% | 0.00% | -0.08% | +0.08% | 0% |

## B-candidates (no trigger yet)

n=753, 20d mean None, rules expectancy 0.0084

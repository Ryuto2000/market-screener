# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-10-19
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 41

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|

First within 60 sessions: -8% stop 0, +16% 0, neither 41. Median MFE 0.6%, median MAE -1.0%, MAE p10 -1.8%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 41 | 49% | 0.7% | -0.8% | -0.06% | 0.85 | None/None | 54% |
| close stop | 41 | 49% | 0.7% | -0.8% | -0.06% | 0.85 | None/None | 54% |

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 41 | 49% | -0.06% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 11 (small) | 45% | 0.03% | None |
| 80-89 | 6 (small) | 83% | 0.98% | None |
| 90-99 | 1 (small) | 0% | 0.00% | None |
| <70 | 22 | 41% | -0.43% | None |
| unknown | 1 (small) | 100% | 0.89% | None |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 20 | 50% | -0.04% | -0.08% | +0.04% | 0% |
| plus:accumulation | 17 (small) | 53% | 0.07% | -0.15% | +0.22% | 0% |
| flags:above_upper_band | 14 (small) | 29% | -0.23% | 0.03% | -0.26% | 0% |
| plus:tight_base | 5 (small) | 40% | 0.04% | -0.07% | +0.11% | 0% |
| flags:macd_fading | 4 (small) | 50% | 0.75% | -0.14% | +0.89% | 0% |
| flags:heavy_selling_day | 1 (small) | 100% | 0.30% | -0.07% | +0.37% | 0% |

## B-candidates (no trigger yet)

n=40, 20d mean None, rules expectancy -0.002

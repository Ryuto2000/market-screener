# Live A-candidates JP

- market: jp, live lists from 2026-10-15 to 2026-10-23
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 201

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 41 | -0.4% | -0.5% | 41% | -4.0% | 3.4% |

First within 60 sessions: -8% stop 2, +16% 0, neither 199. Median MFE 1.3%, median MAE -1.7%, MAE p10 -4.7%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 201 | 37% | 1.6% | -1.6% | -0.42% | 0.59 | 2.5/3.5 | 60% |
| close stop | 201 | 37% | 1.6% | -1.6% | -0.39% | 0.60 | 2.5/None | 60% |

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 201 | 37% | -0.42% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 70-79 | 39 | 36% | -0.72% | None |
| 80-89 | 48 | 44% | -0.04% | None |
| 90-99 | 2 (small) | 0% | 0.00% | None |
| <70 | 111 | 35% | -0.48% | None |
| unknown | 1 (small) | 100% | 0.20% | None |

## signals (intraday-stop expectancy, with vs without)

| signal | n with | win rate with | exp. with | exp. without | diff | stop first (with) |
|---|---|---|---|---|---|---|
| flags:macd_divergence | 100 | 45% | -0.12% | -0.70% | +0.58% | 0% |
| plus:accumulation | 88 | 32% | -0.60% | -0.27% | -0.33% | 1% |
| flags:above_upper_band | 40 | 48% | -0.03% | -0.51% | +0.48% | 0% |
| flags:macd_fading | 37 | 24% | -0.37% | -0.43% | +0.06% | 0% |
| plus:tight_base | 30 | 37% | -0.14% | -0.46% | +0.32% | 0% |
| flags:heavy_selling_day | 4 (small) | 100% | 1.29% | -0.45% | +1.74% | 0% |
| flags:macd_dead_cross | 2 (small) | 0% | -0.72% | -0.41% | -0.31% | 0% |

## B-candidates (no trigger yet)

n=200, 20d mean None, rules expectancy -0.005

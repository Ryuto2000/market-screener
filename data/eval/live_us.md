# Live A-candidates US

- market: us, live lists from 2026-10-16 to 2026-10-16
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 40

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 40 | 2.4% | 2.4% | 82% | -0.5% | 5.5% |
| 10d | 40 | 3.6% | 3.6% | 85% | -0.6% | 7.6% |
| 20d | 40 | 1.0% | 1.0% | 57% | -9.7% | 10.8% |

First within 60 sessions: -8% stop 20, +16% 2, neither 18. Median MFE 8.2%, median MAE -7.4%, MAE p10 -20.0%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 40 | 45% | 5.6% | -6.2% | -0.87% | 0.74 | 11.0/12.0 | 43% |
| close stop | 40 | 45% | 5.5% | -7.3% | -1.54% | 0.62 | 11.0/14.0 | 44% |

Add-on: intraday: added in 25%, add lot mean -2.38% of the initial position; close: added in 25%, add lot mean -2.73% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 40 | 45% | -0.87% | 1.0% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| unknown | 40 | 45% | -0.87% | 1.0% |

## B-candidates (no trigger yet)

n=40, 20d mean 0.0066, rules expectancy 0.0051

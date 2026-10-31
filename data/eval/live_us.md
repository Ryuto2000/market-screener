# Live A-candidates US

- market: us, live lists from 2026-10-16 to 2026-10-16
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 40

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 40 | 2.4% | 2.4% | 82% | -0.5% | 5.5% |
| 10d | 40 | 3.6% | 3.6% | 85% | -0.6% | 7.6% |

First within 60 sessions: -8% stop 2, +16% 0, neither 38. Median MFE 5.5%, median MAE -1.7%, MAE p10 -4.6%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 40 | 85% | 4.4% | -3.2% | 3.24% | 7.80 | 6.0/6.0 | 26% |
| close stop | 40 | 85% | 4.4% | -3.2% | 3.25% | 7.85 | 6.0/7.0 | 26% |

Add-on: intraday: added in 5%, add lot mean -0.21% of the initial position; close: added in 5%, add lot mean -0.21% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 40 | 85% | 3.24% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| unknown | 40 | 85% | 3.24% | None |

## B-candidates (no trigger yet)

n=40, 20d mean None, rules expectancy 0.0201

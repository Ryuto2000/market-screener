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

First within 60 sessions: -8% stop 15, +16% 2, neither 23. Median MFE 7.4%, median MAE -5.2%, MAE p10 -17.9%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 40 | 52% | 6.0% | -5.9% | 0.40% | 1.14 | 11.0/12.0 | 39% |
| close stop | 40 | 55% | 6.1% | -6.8% | 0.33% | 1.11 | 11.0/13.0 | 37% |

Add-on: intraday: added in 22%, add lot mean -1.57% of the initial position; close: added in 22%, add lot mean -1.60% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 40 | 52% | 0.40% | 1.0% |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| unknown | 40 | 52% | 0.40% | 1.0% |

## B-candidates (no trigger yet)

n=40, 20d mean 0.0066, rules expectancy 0.0218

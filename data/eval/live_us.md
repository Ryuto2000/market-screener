# Live A-candidates US

- market: us, live lists from 2026-10-16 to 2026-10-16
- every A and B name is followed whether or not it was bought; entry at the next open after the list date
- young signals have only a few sessions; horizons without data are left out

Signals: 40

| horizon | n | mean | median | % up | p10 | p90 |
|---|---|---|---|---|---|---|
| 5d | 40 | 2.4% | 2.4% | 82% | -0.5% | 5.5% |
| 10d | 40 | 3.6% | 3.6% | 85% | -0.6% | 7.6% |

First within 60 sessions: -8% stop 14, +16% 1, neither 25. Median MFE 7.1%, median MAE -4.7%, MAE p10 -15.2%.

| exit rules | n | win rate | avg win | avg loss | expectancy | profit factor | days (win/loss) | top 10% share of profit |
|---|---|---|---|---|---|---|---|---|
| intraday stop | 40 | 50% | 4.6% | -5.7% | -0.53% | 0.81 | 11.0/12.0 | 37% |
| close stop | 40 | 52% | 4.5% | -7.0% | -0.99% | 0.70 | 11.0/13.0 | 36% |

Add-on: intraday: added in 22%, add lot mean -2.25% of the initial position; close: added in 22%, add lot mean -2.55% of the initial position.

## by_year

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| 2026 | 40 | 50% | -0.53% | None |

## by_rs_rating

| group | n | win rate | expectancy | 20d mean |
|---|---|---|---|---|
| unknown | 40 | 50% | -0.53% | None |

## B-candidates (no trigger yet)

n=40, 20d mean None, rules expectancy 0.0092

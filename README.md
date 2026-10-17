# market-screener

A small, rules-based momentum screener for **Tokyo Stock Exchange** and **US (S&P 500 / S&P 400)** stocks.
It runs on GitHub Actions every weekday and commits its results as JSON, so the output can be read by people,
spreadsheets or other programs without running anything locally.

Most open-source momentum screeners (Minervini "trend template" style) cover US stocks only. This one also
covers all domestic stocks listed on the TSE Prime, Standard and Growth markets.

> Not investment advice. The output is a mechanical filter on free, unofficial data and can be wrong or late.

## Schedule

| Run | When (UTC) | Notes |
|---|---|---|
| Japan | 06:35 Mon–Fri (15:35 JST) | after the 15:30 close; takes about 10 minutes |
| US | 22:15 Mon–Fri | after the close in both summer and winter time |
| Manual | Actions → `screen` → Run workflow | input `jp` or `us` |

## What it checks

| Step | Rule |
|---|---|
| Universe | JP: JPX listed-issues file (Prime/Standard/Growth, domestic stocks). US: S&P 500 + S&P 400 (Wikipedia) |
| Liquidity | 20-day average turnover ≥ ¥300M / $20M, market cap ≥ ¥10B / $2B |
| History | ≥ 220 sessions (also excludes recent IPOs) |
| Trend | 50-day SMA > 200-day SMA, close > 50-day SMA, 200-day SMA rising over 20 sessions, within 15% of the 52-week high |
| Relative strength | 6-month return beats the benchmark (TOPIX ETF 1306 / SPY); `rs_rating` = 1–99 percentile of 0.4×3m + 0.2×(6m+9m+12m) return |
| Trigger | **a** close above the prior 3-month high within the last 3 sessions on ≥1.5× 50-day volume · **b** within 3% of the 3-month high · **c** breakout within 4 weeks, pullback to the breakout level or 20-day SMA (±3%), then an up close |
| Chase limit | a: breakout level +3% · b: 3-month high +3% · c: pullback low +3% |
| Fundamentals (US) | latest quarter revenue and operating income up year over year |
| Earnings | at least 5 sessions to the next report (when known) |
| Flags | `fin_unknown`, `wide_stop` (structural stop >15% away), `crypto_related`, `turnover_gt_mcap` (speculative spike), `volume_spike_5x` |

`rank_hint`: **A** = every check passes, **B** = everything except the trigger. `trigger_but_failed` lists names with a trigger that failed another check.

## Outputs (`data/`)

| File | Content |
|---|---|
| `jp.json`, `us.json` | `A` (top 40), `B` (top 40), `trigger_but_failed`, `market_regime` (benchmark trend and breadth), counts, errors |
| `prices_jp.json`, `prices_us.json` | price table for every priced ticker plus `extras.txt` (indices, FX, common ETFs). Keys: `d` date, `c` close, `pc` previous close, `h`/`l` high/low, `v` volume, `s20`/`s50`/`s200` SMAs, `h3m`/`h52` highs, `rsi` RSI(14), `r6m` 6-month return, `c60` last 60 closes (oldest first), `n` name |
| `history/<date>_<market>.json` | daily A/B lists, for checking how the picks did later |
| `logs/` | log of the latest run |

## Data caveats

- Prices come from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance) (unofficial). It can break or lag.
- Yahoo often leaves the latest Tokyo daily bar empty for hours after the close; the screener rebuilds that session from 60-minute bars, so its close can differ slightly from the official close.
- Quarterly fundamentals for most Tokyo listings are not available from Yahoo, so JP results carry `fin_unknown`.
- Prices are actual traded prices (split-adjusted, not dividend-adjusted).

## Running locally

```bash
pip install -r requirements.txt
python -m pytest -q tests
python -m screener.run --market jp   # or us
```

## Privacy

The repository holds only public market data and screening code. No account, portfolio or personal data is stored or needed; the workflow uses only the default `GITHUB_TOKEN`.

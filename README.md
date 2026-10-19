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
| Secondary (shown, not filtered) | `rsi14`, `macd` / `macd_signal` / `macd_hist` (12-26-9) and its 3-session change, Bollinger `%b` (20, 2), `pct_above_sma200`, `day_range_pos`. Flags: `overheat` (RSI > 80 or > 40% above the 200-day SMA), `above_upper_band`, `macd_fading` (positive histogram shrinking 2 sessions in a row), `macd_dead_cross`, `macd_divergence` (higher closing high with a lower MACD than at the prior peak within 120 sessions), `heavy_selling_day` (down day closing in the bottom 30% of its range on ≥ 1.5× volume) |
| Structure (shown, not filtered) | `atr14`, `atr_pct`, `stop_atr_mult` (distance to the −8% stop in ATRs), power gap (`gap_date`, `gap_pct`, `gap_held`: open ≥ +4% on ≥ 2× volume in the last 20 sessions), base before the breakout (`base_depth`, `base_vol_dryup`, `base_range_contraction`), `updown_vol_50` (volume on up days ÷ down days). Supportive signals go to `plus`: `power_gap`, `tight_base` (depth ≤ 25%, volume and volatility drying up), `accumulation` (up/down volume ≥ 1.5). Warnings go to `flags`: `stop_inside_noise` (stop < 2 ATR away), `pinned_price` (10-session close range < 1% and ATR < 1%: likely a tender offer or merger; excluded in both markets), `gap_filled`, `deep_base` (> 35%), `distribution` (up/down volume < 0.8) |
| Market | `market_regime.benchmark_distribution_days_25`: sessions in the last 25 where the benchmark ETF fell ≥ 0.2% on higher volume; `caution` when ≥ 5 |

**Market rules from the backtest** (`screener/rules.py`, check `backtest_rules`): Japan excludes `stop_inside_noise`, `deep_base`, `overheat` and RS rating ≥ 95, ranks by lower volatility, and treats power gaps as information only. The US requires RS rating ≥ 90, the benchmark in an uptrend and fewer than 5 distribution days. A-candidates need an `a_breakout` trigger (the only entry type the backtest supports so far, `rules.VALIDATED_TRIGGERS`); names with only `b_near_high` or `c_pullback` are listed as B. The backtest also replays (b) and (c) entries for comparison ("Entry types" table). `market_regime.risk_per_trade` is the share of assets to risk on a new trade: 0.5% in Japan when ≥ 75% of liquid names close above their 50-day SMA, otherwise 0.3%.

`rank_hint`: **A** = every check passes, **B** = everything except the trigger. `trigger_but_failed` lists names with a trigger that failed another check. The secondary indicators never change `rank_hint`; they are there for review and to test later (with `history/`) whether any of them predicts weaker follow-through.

## Outputs (`data/`)

| File | Content |
|---|---|
| `jp.json`, `us.json` | `A` (top 40), `B` (top 40), `trigger_but_failed`, `market_regime` (benchmark trend and breadth), counts, errors |
| `prices_jp.json`, `prices_us.json` | price table for every priced ticker plus `extras.txt` (indices, FX, common ETFs). Keys: `d` date, `c` close, `pc` previous close, `h`/`l` high/low, `v` volume, `s20`/`s50`/`s200` SMAs, `h3m`/`h52` highs, `rsi` RSI(14), `r6m` 6-month return, `c60` and `h60` last 60 closes and highs (oldest first), `n` name, `cs` source of the latest close (`d` daily bar, `o` official quote, `h` hourly rebuild) |
| `history/<date>_<market>.json` | daily A/B lists, for checking how the picks did later |
| `logs/` | log of the latest run |

## Evaluation

Every Saturday (`evaluate` workflow) two things are measured, so the rules can be checked against data instead of anecdotes:

- **Backtest** (`python -m screener.backtest --market jp`): the screener is replayed over five years of daily data. Each day a stock passes the trend, relative-strength, liquidity and breakout-with-volume rules (within the chase limit), a trade is entered at the next open and followed.
- **Live follow-up** (`python -m screener.evaluate --market jp`): every A and B name from `data/history/` is followed from the next open after its list date, whether or not anyone bought it.

Each signal gets returns after 5/10/20/40/60 sessions, the largest gain and drawdown within 60 sessions, whether −8% or +16% came first, and the result of the exit rules (−8% stop; at a close ≥ +8% the stop goes to entry +1% and then trails 10% under the highest high, never down; no partial profit taking; one add-on of half the initial size at the next open when that close is also above the prior 3-month high; returns are on the initial position; the previous ladder is kept as `simulate.OLD_RULES`), simulated with a resting stop order and with a close-only stop. `screener.variants` replays the same signals with the previous rules and variations of the current ones (stop width, break-even level, trailing width, add-on size, partial profit taking). Results are split by year, market regime, distribution days, RS rating and each flag (`data/eval/*.md`, `*.json`, per-signal `*.csv`).

Limits: no point-in-time market cap, fundamentals or earnings dates; today's listings only (survivorship bias makes the backtest look somewhat better than reality).

## Data caveats

- Prices come from Yahoo Finance via [yfinance](https://github.com/ranaroussi/yfinance) (unofficial). It can break or lag.
- Yahoo often leaves the latest Tokyo daily bar empty for hours after the close. The screener rebuilds that session from 60-minute bars and then replaces the close, high, low and volume with Yahoo's official quote (`cs` = `o`). If the quote is unavailable the hourly value stays (`cs` = `h`) and can differ slightly from the official close.
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

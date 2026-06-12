# 2026-05-19 Registered Portfolio Snapshot

This reference captures the extraction/calculation pattern from a session where the user provided brokerage screenshots and a cash update.

## User-provided accounts

### Wealthsimple RRSP

Visible holdings in USD:

- FIG: 10 shares, market value $231.30 USD, P&L -52.83%
- GOOG: 8 shares, market value $3,079.60 USD, P&L +127.15%
- META: 9 shares, market value $5,417.82 USD, P&L -4.43%
- NVDA: 241 shares, market value $53,453.80 USD, P&L +138.01%
- PLTR: 3 shares, market value $404.43 USD, P&L +8.87%
- RACE: 21 shares, market value $6,921.60 USD, P&L -18.61%

Computed holdings total: $69,508.55 USD.

Cash available:

- Total available to trade: $60,714.71 CAD
- CAD cash: $15.18 CAD
- USD cash: $44,116.56 USD
- Implied USD/CAD from cash screen: 1.37589

Computed account estimate:

- Cash + holdings: $113,625.11 USD + $15.18 CAD
- Estimated total RRSP value: ~$156,350.82 CAD
- Cash allocation: ~38.8%
- NVDA allocation within WS RRSP including cash: ~47.0%

### Questrade FHSA

- Total equity: $17,383.04 CAD
- Cash: $11,455.91 CAD
- Market value: $5,927.13 CAD
- Holding: VFV.TO, 33 shares
- Last: $179.61 CAD
- Avg cost: $146.4969 CAD
- Open P&L: +$1,092.73 / +22.60%

Computed allocation:

- Cash: 65.9%
- VFV.TO: 34.1%

### Questrade Spousal RRSP

Account summary:

- Total equity: $6,408.14 CAD
- Cash: $512.11 CAD
- Buying power: $500.85 CAD
- Market value: $5,896.03 CAD
- Open P&L: +$731.02
- Today's P&L: -$133.29 / -2.04%
- Total P&L: +$1,408.14

Holdings shown in USD:

- FIG: 17 shares, value $393.04 USD, last $23.12, avg $71.3817, open P&L -$820.44 / -67.61%
- GOOG: 7 shares, value $2,693.87 USD, last $384.84, avg $173.037, open P&L +$1,482.62 / +122.40%
- META: 2 shares, value $1,204.38 USD, last $602.19, avg $667.2477, open P&L -$130.11 / -9.75%

Computed allocation using implied FX from account market value:

- Cash: 8.0%
- Invested: 92.0%
- GOOG: ~57.8%
- META: ~25.8%
- FIG: ~8.4%

### Questrade RSP

- User stated $20,000 CAD sitting in Questrade RSP cash.

## Combined registered estimate

Using the above screenshots and user-provided cash:

- Wealthsimple RRSP: ~$156,350.82 CAD
- Questrade FHSA: $17,383.04 CAD
- Questrade Spousal RRSP: $6,408.14 CAD
- Questrade RSP cash: $20,000 CAD
- Total registered assets tracked: ~$200,142 CAD

Cash total:

- WS RRSP cash: $60,714.71 CAD equiv
- FHSA cash: $11,455.91 CAD
- Spousal RRSP cash: $512.11 CAD
- Questrade RSP cash: $20,000 CAD
- Total cash: ~$92,682.73 CAD
- Cash allocation: ~46.3%

NVDA exposure:

- NVDA value: $53,453.80 USD * 1.37589 = ~$73,546.55 CAD
- NVDA as % of registered assets: ~36.8%

## Communication pattern that worked

- Acknowledge with `Logged.`
- Then provide concise bullets: totals, cash, holdings, allocation, one risk observation.
- For this user's Telegram style, avoid tables and long explanations.

## Reusable calculation checks

- `cash_pct = cash / total_equity`
- `holding_pct = market_value / total_equity`
- `implied_fx = CAD_total_or_market_value / sum(USD_components)` when all components are known and there are no hidden positions.
- `combined_registered = sum(account_values_CAD)`
- `total_cash_pct = total_cash_CAD / combined_registered`
- `single_stock_pct = single_stock_value_CAD / combined_registered`

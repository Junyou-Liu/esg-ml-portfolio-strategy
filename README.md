# ESG ML Portfolio Strategy

This repository contains an academic ESG ETF allocation and backtesting project built with Python, LumiBot, Yahoo Finance data, and optional Alpaca paper-trading support. It combines machine-learning regime detection, core-satellite portfolio construction, and rule-based rebalancing. It is a research prototype, not investment advice or a live trading record.

## What This Project Shows

- Built a two-level ESG ETF allocation framework with regime detection and core-satellite selection.
- Used Random Forest / Logistic Regression signals from lagged returns, RSI, realized volatility, and short-horizon pullback risk.
- Allocated across broad ESG ETFs (`ESGU`, `VSGX`, `SUSA`), green-theme ETFs (`ICLN`, `TAN`, `LIT`, `QCLN`), and a defensive Treasury ETF (`SHY`).
- Added risk controls: regime-based equity budget, satellite sleeve limits, defensive allocation, drift tolerance, and minimum trade-size filters.
- Preserved executable strategy code, a QuantStats/LumiBot tear sheet, a pitch deck, a roadshow script, and strategy notes.

## Strategy Logic

The project separates the decision process into two layers.

1. Regime detection
   - Uses `ESGU` as the ESG market proxy.
   - Trains on recent price features such as lagged returns, RSI, volatility, and pullback-risk labels.
   - Maps model probabilities into `RISK_ON`, `NEUTRAL`, and `RISK_OFF`.

2. Portfolio construction
   - Selects the strongest names inside broad ESG and green-theme sleeves using six-month momentum.
   - Applies a 70/30 split across the two selected names in each sleeve.
   - Shifts exposure into `SHY` and cash under defensive regimes.
   - Trades only when drift and minimum trade-size checks are met.

## Backtest Snapshot

The saved tear sheet covers 3 Jan 2020 to 30 Dec 2025 and compares the strategy with SPY.

| Metric | Strategy |
| --- | ---: |
| Annual return | 8.19% |
| Annualized volatility | 18.05% |
| Max drawdown | -32.55% |
| Sharpe ratio | 0.33 |
| Sortino ratio | 0.45 |
| Reported beta vs. benchmark | -0.01 |

SPY delivered a higher annual return over the same sample. The useful takeaway is therefore not a benchmark-beating claim; it is the documented process for ESG allocation, risk budgeting, regime-aware exposure control, and reproducible backtesting.

## Repository Structure

```text
.
|-- backtest.py
|-- paper_trade.py
|-- config.py
|-- requirements.txt
|-- strategies/
|   |-- strategy.py
|   `-- example_strategy_*.py
|-- results/
|   `-- backtest-tearsheet-2020-2025.html
`-- docs/
    |-- esg-ml-portfolio-pitch-deck.pdf
    |-- fund-roadshow-presentation-script.pdf
    `-- trading-strategy-notes-cn.docx
```

## Reproduce

```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
python backtest.py
```

Optional Alpaca paper trading requires local credentials in `.env`. Leave `.env.example` blank and never commit real keys.

```bash
ALPACA_API_KEY=
ALPACA_API_SECRET=
```

## Scope and Limits

Historical backtests are sensitive to data source, parameter choice, transaction assumptions, and market regime. This repository should be read as evidence of systematic strategy design and risk-control implementation, not as a recommendation to buy or trade any ETF.

## Stack

Python, LumiBot, QuantStats, scikit-learn, pandas, Yahoo Finance data, Alpaca paper-trading interface, and PowerPoint/PDF reporting.

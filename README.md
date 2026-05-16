# ESG ML Portfolio Strategy

A research prototype for ESG-aware equity selection, portfolio backtesting, and paper-trading validation.

This project is designed for sustainable-finance research and simulated strategy evaluation. It is not investment advice, a live fund product, or a live trading record.

## Project Overview

This repository contains an academic ESG ETF allocation and backtesting project built with Python, LumiBot, Yahoo Finance data, and optional Alpaca paper-trading support. It combines machine-learning regime detection, core-satellite portfolio construction, and rule-based rebalancing.

The main purpose is to show how ESG and climate-transition themes can be translated into a measurable portfolio research workflow while keeping benchmark comparison, drawdown review, and simulation boundaries explicit.

## Tech Stack

| Area | Tools |
| --- | --- |
| Language | Python |
| Backtesting | LumiBot, QuantStats |
| Modeling | scikit-learn |
| Data | pandas, Yahoo Finance data |
| Paper Trading | Alpaca paper-trading interface |
| Reporting | HTML tear sheet, PDF pitch deck, strategy notes |

## Key Features

- Built a two-level ESG ETF allocation framework with regime detection and core-satellite selection.
- Used Random Forest and Logistic Regression signals from lagged returns, RSI, realized volatility, and pullback-risk labels.
- Allocated across broad ESG ETFs (`ESGU`, `VSGX`, `SUSA`), green-theme ETFs (`ICLN`, `TAN`, `LIT`, `QCLN`), and a defensive Treasury ETF (`SHY`).
- Added risk controls including regime-based equity budget, satellite sleeve limits, defensive allocation, drift tolerance, and minimum trade-size filters.
- Preserved executable strategy code, a QuantStats / LumiBot tear sheet, a pitch deck, a roadshow script, and strategy notes.

## Methodology

The strategy separates the decision process into two layers.

1. Regime detection
   - Uses `ESGU` as the ESG market proxy.
   - Trains on recent price features such as lagged returns, RSI, volatility, and pullback-risk labels.
   - Maps model probabilities into `RISK_ON`, `NEUTRAL`, and `RISK_OFF`.

2. Portfolio construction
   - Selects the strongest names inside broad ESG and green-theme sleeves using six-month momentum.
   - Applies a 70/30 split across the two selected names in each sleeve.
   - Shifts exposure into `SHY` and cash under defensive regimes.
   - Trades only when drift and minimum trade-size checks are met.

## Results / Metrics

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

## How to Run

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python backtest.py
```

Optional Alpaca paper trading requires local credentials in `.env`. Leave `.env.example` blank and never commit real keys.

```bash
ALPACA_API_KEY=
ALPACA_API_SECRET=
```

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

## Limitations

- Historical backtests are sensitive to data source, parameter choice, transaction assumptions, and market regime.
- Paper trading is used only as a simulated validation environment, not as live capital deployment.
- The project should not be described as a live fund, a fundraising record, or a recommendation to buy or trade any ETF.
- The strongest interview angle is sustainable-finance research design: ESG screening, risk budgeting, benchmark comparison, and transparent limits.

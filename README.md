# FinAI Innovators: AI-Driven ESG Allocation Strategy

This repository contains a systematic ESG ETF allocation strategy built for the NUS QF5208 AI and FinTech group project. The project combines machine-learning regime detection, core-satellite portfolio construction, and rule-based execution in LumiBot, with optional Alpaca paper-trading support.

The strategy is designed as an academic research and backtesting project. It is not investment advice and is not a live trading recommendation.

## Project Highlights

- Built a two-level ESG portfolio strategy in Python using LumiBot, Yahoo Finance backtesting data, and optional Alpaca paper trading.
- Used Random Forest / Logistic Regression signals to estimate market regime from an ESG broad-market proxy (`ESGU`).
- Allocated dynamically across broad ESG ETFs (`ESGU`, `VSGX`, `SUSA`), green-theme ETFs (`ICLN`, `TAN`, `LIT`, `QCLN`), and a defensive Treasury ETF (`SHY`).
- Added practical risk controls, including regime-based equity budget, satellite sleeve limits, defensive allocation, drift tolerance, and minimum trade-size filters.
- Preserved full project evidence: strategy code, backtest report, trade report, pitch deck, roadshow script, and project video.

## Strategy Logic

The strategy separates the investment decision into two layers.

**1. Regime detection**

The model uses `ESGU` as the ESG market proxy and trains on recent price features:

- lagged daily returns,
- 14-day RSI,
- 10-day realized volatility,
- a secondary seven-day pullback-risk classifier.

The model maps probability estimates into three regimes:

- `RISK_ON`: higher equity allocation with more satellite exposure,
- `NEUTRAL`: balanced ESG core allocation,
- `RISK_OFF`: reduced equity exposure with a larger `SHY` defensive sleeve.

**2. Portfolio construction**

Within each sleeve, the strategy ranks ETFs by six-month momentum and selects the top two names. Target weights are then built from:

- a regime-dependent equity budget,
- a regime-dependent satellite share,
- a 70/30 allocation split between the two strongest names in each sleeve,
- defensive allocation to `SHY` and residual cash.

## Backtest Snapshot

The included LumiBot / QuantStats report covers January 2020 to December 2025.

| Metric | Strategy |
| --- | ---: |
| Total return | 60% |
| Annual return | 8.19% |
| Annualized volatility | 18.05% |
| Max drawdown | -32.55% |
| Sharpe ratio | 0.33 |
| Sortino ratio | 0.45 |
| Reported beta vs benchmark | -0.01 |

The benchmark in the generated tear sheet is SPY. This project is presented as a transparent strategy-design and backtesting exercise rather than a benchmark-beating claim: SPY delivered higher absolute return over this sample, while the strategy demonstrates a distinct ESG allocation framework with near-zero reported benchmark beta, explicit downside controls, and a documented decision process.

## Repository Structure

```text
.
+-- backtest.py                         # Reproducible Yahoo Finance backtest entry point
+-- paper_trade.py                      # Optional Alpaca paper-trading entry point
+-- config.py                           # Environment-based Alpaca configuration
+-- requirements.txt                    # Python dependencies
+-- strategies/
|   +-- strategy.py                     # Main two-level ESG strategy
|   +-- example_strategy_*.py           # Course reference strategies
+-- results/
|   +-- backtest-tearsheet-2020-2025.html
|   +-- backtest-trades-2020-2025.html
+-- docs/
|   +-- finai-innovators-esg-fund-pitch-deck.pdf
|   +-- fund-roadshow-presentation-script.pdf
|   +-- trading-strategy-notes-cn.docx
+-- media/
|   +-- finai-esg-roadshow-video.mp4
+-- RESUME_SUMMARY.md
```

## Quick Start

Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies.

```bash
python -m pip install -r requirements.txt
```

Run the backtest.

```bash
python backtest.py
```

The generated output can be compared with the saved reports in `results/`.

## Optional Paper Trading

Paper trading requires an Alpaca paper account. Create a local `.env` file from `.env.example`:

```bash
ALPACA_API_KEY=YOUR_ALPACA_API_KEY
ALPACA_API_SECRET=YOUR_ALPACA_API_SECRET
```

Then run:

```bash
python paper_trade.py
```

Only paper-trading credentials should be used. Do not commit `.env` or any API keys.

## Project Artifacts

- [Backtest tear sheet](results/backtest-tearsheet-2020-2025.html)
- [Backtest trades report](results/backtest-trades-2020-2025.html)
- [Pitch deck](docs/finai-innovators-esg-fund-pitch-deck.pdf)
- [Roadshow script](docs/fund-roadshow-presentation-script.pdf)
- [Strategy notes](docs/trading-strategy-notes-cn.docx)
- [Roadshow video](media/finai-esg-roadshow-video.mp4)

## Disclaimer

This repository is for academic and portfolio demonstration purposes only. Historical backtests are sensitive to data source, parameter choice, transaction assumptions, and market regime. The project should be read as evidence of systematic strategy design and implementation, not as an investment recommendation.

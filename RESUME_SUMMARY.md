# Resume Project Summary

## English Version

**AI-Driven ESG Allocation Strategy | Python, LumiBot, Alpaca, Machine Learning**

- Designed a two-level ESG ETF allocation strategy combining machine-learning regime detection and core-satellite portfolio construction.
- Built Random Forest / Logistic Regression signals from lagged returns, RSI, volatility, and seven-day pullback risk to classify market regimes.
- Implemented dynamic allocation across broad ESG ETFs, green-theme ETFs, Treasury defense, and cash, with risk-budget, drift-tolerance, and minimum trade-size controls.
- Backtested the strategy on Yahoo Finance data from 2020 to 2025 in LumiBot, producing a 60% total return, 8.19% annual return, 18.05% annualized volatility, and -32.55% max drawdown in the saved report.
- Prepared complete project deliverables, including executable code, backtest tear sheet, trade report, pitch deck, roadshow script, and presentation video.

## 中文版本

**AI 驱动 ESG 资产配置策略 | Python, LumiBot, Alpaca, 机器学习**

- 设计两层 ESG ETF 配置策略，将机器学习市场状态识别与核心-卫星资产配置框架结合。
- 基于滞后收益率、RSI、波动率及 7 日回撤风险构建 Random Forest / Logistic Regression 信号，用于识别 `RISK_ON`、`NEUTRAL`、`RISK_OFF` 三类市场状态。
- 实现宽基 ESG ETF、绿色主题 ETF、短久期国债 ETF 与现金之间的动态配置，并加入风险预算、调仓漂移阈值及最小交易规模控制。
- 使用 LumiBot 和 Yahoo Finance 数据完成 2020-2025 年回测，报告显示策略总收益 60%、年化收益 8.19%、年化波动率 18.05%、最大回撤 -32.55%。
- 整理完整项目交付物，包括可运行代码、回测 tear sheet、交易明细、路演 PPT、演讲稿及展示视频。

## Interview Talking Points

- This is an academic backtesting and paper-trading framework, not a live fund or personal trading account.
- The key design choice is separating regime judgment from ETF selection, which makes the strategy logic easier to explain and audit.
- The backtest does not claim to outperform SPY on absolute return. Its main value is a structured ESG allocation process with explicit risk controls and reproducible evidence.

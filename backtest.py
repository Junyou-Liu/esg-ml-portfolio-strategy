from datetime import datetime

from lumibot.backtesting import YahooDataBacktesting

from strategies.strategy import Strategy


BACKTEST_START = datetime(2020, 1, 1)
BACKTEST_END = datetime(2025, 12, 31)
INITIAL_BUDGET = 100_000


def run_backtest():
    """Run the ESG strategy on Yahoo Finance historical data."""
    Strategy.backtest(
        YahooDataBacktesting,
        BACKTEST_START,
        BACKTEST_END,
        budget=INITIAL_BUDGET,
    )


if __name__ == "__main__":
    run_backtest()

from lumibot.brokers import Alpaca
from lumibot.traders import Trader

from config import require_alpaca_config
from strategies.strategy import Strategy


def run_paper_trading():
    """Run the strategy against an Alpaca paper-trading account."""
    broker = Alpaca(require_alpaca_config())
    strategy = Strategy(broker=broker)

    trader = Trader()
    trader.add_strategy(strategy)
    trader.run_all()


if __name__ == "__main__":
    run_paper_trading()

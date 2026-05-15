import os

from dotenv import load_dotenv


load_dotenv()

ALPACA_CONFIG = {
    "API_KEY": os.getenv("ALPACA_API_KEY"),
    "API_SECRET": os.getenv("ALPACA_API_SECRET"),
    "PAPER": True,
}


def require_alpaca_config():
    """Return Alpaca config after validating that paper-trading keys exist."""
    missing = [key for key in ("API_KEY", "API_SECRET") if not ALPACA_CONFIG.get(key)]
    if missing:
        joined = ", ".join(missing)
        raise RuntimeError(
            f"Missing Alpaca paper-trading credential(s): {joined}. "
            "Create a .env file from .env.example before running paper_trade.py."
        )
    return ALPACA_CONFIG

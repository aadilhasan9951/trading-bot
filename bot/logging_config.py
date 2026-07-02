import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't already exist
_log_dir = Path("logs")
_log_dir.mkdir(exist_ok=True)

LOG_FILE = str(_log_dir / "trading_bot.log")


def setup_logging():
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # File handler - captures everything (debug + above)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    # Console handler - only info and above
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

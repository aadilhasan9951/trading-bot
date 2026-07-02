#!/usr/bin/env python3
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)

logger = setup_logging()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py BTCUSDT BUY MARKET 0.001
  python cli.py BTCUSDT SELL LIMIT 0.001 50000
  python cli.py BTCUSDT BUY STOP_LIMIT 0.001 50000 49000
        """,
    )
    parser.add_argument("symbol", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("type", choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("quantity", help="Order quantity")
    parser.add_argument("price", nargs="?", default=None, help="Price (required for LIMIT and STOP_LIMIT)")
    parser.add_argument("stop_price", nargs="?", default=None, help="Stop price (required for STOP_LIMIT)")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price) if args.type in ("LIMIT", "STOP_LIMIT") else None
        stop_price = validate_price(args.stop_price) if args.type == "STOP_LIMIT" else None
    except ValueError as e:
        logger.error("Validation error: %s", e)
        print(f"Error: {e}")
        sys.exit(1)

    if order_type in ("LIMIT", "STOP_LIMIT") and price is None:
        logger.error("Price is required for %s orders", order_type)
        print(f"Error: Price is required for {order_type} orders")
        sys.exit(1)

    if order_type == "STOP_LIMIT" and stop_price is None:
        logger.error("Stop price is required for STOP_LIMIT orders")
        print("Error: Stop price is required for STOP_LIMIT orders")
        sys.exit(1)

    print(f"\n{'=' * 50}")
    print("ORDER REQUEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Symbol:      {symbol}")
    print(f"Side:        {side}")
    print(f"Type:        {order_type}")
    print(f"Quantity:    {quantity}")
    if price:
        print(f"Price:       {price}")
    if stop_price:
        print(f"Stop Price:  {stop_price}")
    print(f"{'=' * 50}\n")

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API credentials")
        print("Error: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
        sys.exit(1)

    try:
        client = BinanceFuturesClient(api_key, api_secret)
        manager = OrderManager(client)

        if order_type == "MARKET":
            manager.place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            manager.place_limit_order(symbol, side, quantity, price)
        elif order_type == "STOP_LIMIT":
            manager.place_stop_limit_order(symbol, side, quantity, price, stop_price)

    except Exception as e:
        logger.exception("Failed to place order")
        print(f"X Failed to place order: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

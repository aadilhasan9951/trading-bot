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


def get_api_credentials():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API credentials")
        print("Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set as environment variables")
        sys.exit(1)

    return api_key, api_secret


def interactive_mode():
    print("\n--- Interactive Order Entry ---\n")

    while True:
        symbol_raw = input("Enter symbol (e.g. BTCUSDT): ").strip()
        try:
            symbol = validate_symbol(symbol_raw)
            break
        except ValueError as e:
            print(f"  Invalid: {e}")

    while True:
        side_raw = input("Enter side (BUY/SELL): ").strip()
        try:
            side = validate_side(side_raw)
            break
        except ValueError as e:
            print(f"  Invalid: {e}")

    while True:
        type_raw = input("Enter order type (MARKET/LIMIT): ").strip()
        try:
            order_type = validate_order_type(type_raw)
            break
        except ValueError as e:
            print(f"  Invalid: {e}")

    while True:
        qty_raw = input("Enter quantity: ").strip()
        try:
            quantity = validate_quantity(qty_raw)
            break
        except ValueError as e:
            print(f"  Invalid: {e}")

    price = None
    if order_type == "LIMIT":
        while True:
            price_raw = input("Enter limit price: ").strip()
            try:
                price = validate_price(price_raw)
                if price is None:
                    print("  Price is required for LIMIT orders")
                    continue
                break
            except ValueError as e:
                print(f"  Invalid: {e}")

    return symbol, side, order_type, quantity, price


def display_summary(symbol, side, order_type, quantity, price):
    print(f"\n{'=' * 50}")
    print("ORDER REQUEST SUMMARY")
    print(f"{'=' * 50}")
    print(f"Symbol:      {symbol}")
    print(f"Side:        {side}")
    print(f"Type:        {order_type}")
    print(f"Quantity:    {quantity}")
    if price is not None:
        print(f"Price:       {price}")
    print(f"{'=' * 50}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("symbol", nargs="?", help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("side", nargs="?", choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("type", nargs="?", choices=["MARKET", "LIMIT"], help="MARKET or LIMIT")
    parser.add_argument("quantity", nargs="?", help="Order quantity")
    parser.add_argument("price", nargs="?", default=None, help="Price (required for LIMIT)")

    args = parser.parse_args()

    # If no arguments provided, launch interactive mode
    if args.symbol is None:
        symbol, side, order_type, quantity, price = interactive_mode()
    else:
        try:
            symbol = validate_symbol(args.symbol)
            side = validate_side(args.side)
            order_type = validate_order_type(args.type)
            quantity = validate_quantity(args.quantity)
            price = validate_price(args.price) if args.type == "LIMIT" else None
        except ValueError as e:
            logger.error("Validation error: %s", e)
            print(f"Error: {e}")
            sys.exit(1)

        if order_type == "LIMIT" and price is None:
            logger.error("Price is required for LIMIT orders")
            print("Error: Price is required for LIMIT orders")
            sys.exit(1)

    display_summary(symbol, side, order_type, quantity, price)

    api_key, api_secret = get_api_credentials()

    try:
        client = BinanceFuturesClient(api_key, api_secret)
        manager = OrderManager(client)

        if order_type == "MARKET":
            manager.place_market_order(symbol, side, quantity)
        else:
            manager.place_limit_order(symbol, side, quantity, price)

    except Exception as e:
        logger.exception("Failed to place order")
        print(f"X Failed to place order: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

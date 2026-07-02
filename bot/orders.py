import logging
from typing import Any

from bot.client import BinanceFuturesClient

logger = logging.getLogger("trading_bot.orders")


class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict[str, Any]:
        logger.info(f"Placing {side} MARKET order for {quantity} {symbol}")
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        self._print_result(result)
        return result

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict[str, Any]:
        logger.info(f"Placing {side} LIMIT order for {quantity} {symbol} @ {price}")
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )
        self._print_result(result)
        return result

    def _print_result(self, result: dict[str, Any]) -> None:
        order_id = result.get("orderId", "N/A")
        status = result.get("status", "N/A")
        executed_qty = result.get("executedQty", "0.0")
        cum_qty = result.get("cumQty", "0.0")

        # avgPrice might not be present for unfilled orders
        avg_price = result.get("avgPrice")
        if avg_price is None or avg_price in ("0.0", "0.00", ""):
            avg_price = "N/A"

        logger.info(f"Order ID: {order_id} | Status: {status} | Executed: {executed_qty}")

        print(f"\n{'=' * 50}")
        print(f"Order ID:       {order_id}")
        print(f"Status:         {status}")
        print(f"Executed Qty:   {executed_qty}")
        print(f"Cumulative Qty: {cum_qty}")
        if avg_price != "N/A":
            print(f"Avg Price:      {avg_price}")
        print(f"\nSUCCESS - Order placed successfully!")
        print(f"{'=' * 50}\n")

import logging
from typing import Any

from bot.client import BinanceFuturesClient

logger = logging.getLogger("trading_bot.orders")


class OrderManager:
    def __init__(self, client: BinanceFuturesClient):
        self.client = client

    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict[str, Any]:
        logger.info("Placing %s MARKET order for %s %s", side, quantity, symbol)
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        self._print_order_result(result)
        return result

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict[str, Any]:
        logger.info("Placing %s LIMIT order for %s %s @ %s", side, quantity, symbol, price)
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
        )
        self._print_order_result(result)
        return result

    def place_stop_limit_order(
        self, symbol: str, side: str, quantity: float, price: float, stop_price: float
    ) -> dict[str, Any]:
        logger.info(
            "Placing %s STOP_LIMIT order for %s %s, trigger @ %s, limit @ %s",
            side, quantity, symbol, stop_price, price,
        )
        result = self.client.place_order(
            symbol=symbol,
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
        )
        self._print_order_result(result)
        return result

    def _print_order_result(self, result: dict[str, Any]) -> None:
        order_id = result.get("orderId", "N/A")
        status = result.get("status", "N/A")
        executed_qty = result.get("executedQty", "N/A")
        cum_qty = result.get("cumQty", "N/A")
        avg_price = result.get("avgPrice")

        if avg_price is None or avg_price == "0.00":
            avg_price = "N/A"

        logger.info("Order ID: %s", order_id)
        logger.info("Status: %s", status)
        logger.info("Executed Qty: %s", executed_qty)
        logger.info("Cumulative Qty: %s", cum_qty)
        logger.info("Avg Price: %s", avg_price)

        print(f"\n{'=' * 50}")
        print(f"Order ID:       {order_id}")
        print(f"Status:         {status}")
        print(f"Executed Qty:   {executed_qty}")
        print(f"Cumulative Qty: {cum_qty}")
        if avg_price != "N/A":
            print(f"Avg Price:      {avg_price}")
        print(f"\nSUCCESS - Order placed successfully!")
        print(f"{'=' * 50}\n")

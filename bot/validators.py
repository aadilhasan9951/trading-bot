import re


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.strip():
        raise ValueError("Symbol cannot be empty")
    s = symbol.strip().upper()
    if not re.match(r"^[A-Z0-9]{5,}$", s):
        raise ValueError(f"Invalid symbol format: {symbol}")
    return s


def validate_side(side: str) -> str:
    s = side.strip().upper()
    if s not in ("BUY", "SELL"):
        raise ValueError(f"Side must be BUY or SELL, got: {side}")
    return s


def validate_order_type(order_type: str) -> str:
    ot = order_type.strip().upper()
    if ot not in ("MARKET", "LIMIT"):
        raise ValueError(f"Order type must be MARKET or LIMIT, got: {order_type}")
    return ot


def validate_quantity(quantity: str) -> float:
    try:
        q = float(quantity)
    except (ValueError, TypeError):
        raise ValueError(f"Quantity must be a valid number, got: {quantity}")
    if q <= 0:
        raise ValueError(f"Quantity must be greater than 0, got: {q}")
    return q


def validate_price(price: str) -> float | None:
    if price is None or price.strip() == "":
        return None
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError(f"Price must be a valid number, got: {price}")
    if p <= 0:
        raise ValueError(f"Price must be greater than 0, got: {p}")
    return p

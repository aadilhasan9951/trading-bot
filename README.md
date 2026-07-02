# Binance Futures Testnet Trading Bot

A command-line application to place MARKET and LIMIT orders on Binance Futures Testnet (USDT-M).

## Prerequisites

- Python 3.x installed
- A Binance Futures Testnet account (register at https://testnet.binancefuture.com)
- API Key and Secret generated from the testnet dashboard

## Setup

Set your API credentials as environment variables:

```powershell
$env:BINANCE_API_KEY="your_api_key_here"
$env:BINANCE_API_SECRET="your_api_secret_here"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can pass arguments directly or run without arguments for interactive mode.

### Command-line mode

```bash
# Market Buy
python cli.py BTCUSDT BUY MARKET 0.001

# Limit Sell
python cli.py BTCUSDT SELL LIMIT 0.001 60000
```

### Interactive mode

```bash
python cli.py
```

This will prompt you for each input step by step with validation.

### Arguments

| Position | Name       | Required For        | Description                    |
|----------|------------|---------------------|--------------------------------|
| 1        | symbol     | All                 | Trading pair (e.g. BTCUSDT)    |
| 2        | side       | All                 | BUY or SELL                    |
| 3        | type       | All                 | MARKET or LIMIT                |
| 4        | quantity   | All                 | Order quantity in base asset   |
| 5        | price      | LIMIT               | Limit price in quote asset     |

### Output

The bot prints a summary of your request followed by the API response showing order ID, status, executed quantity, and average price.

```
==================================================
ORDER REQUEST SUMMARY
==================================================
Symbol:      BTCUSDT
Side:        BUY
Type:        MARKET
Quantity:    0.001
==================================================

==================================================
Order ID:       18381706284
Status:         NEW
Executed Qty:   0.0000
Cumulative Qty: 0.0000

SUCCESS - Order placed successfully!
==================================================
```

## Project Structure

```
trading_bot/
  bot/
    client.py          # API client with HMAC authentication
    orders.py          # Order placement logic
    validators.py      # Input validation helpers
    logging_config.py  # Logging setup
  cli.py               # Entry point (argparse with interactive fallback)
  logs/
    trading_bot.log    # Generated on each run
  README.md
  requirements.txt
```

## Logging

All API requests, responses, and errors are logged to `logs/trading_bot.log` with timestamps and log levels. Console output shows INFO level while the file captures DEBUG level details including raw API responses.

## Error Handling

- Invalid inputs (bad symbol, non-numeric quantity, etc.) are caught and reported before any API call
- API errors return the error code and message from Binance
- Network timeouts and connection failures are handled gracefully
- Each error is logged to the file with stack trace

## Assumptions

- Using USDT-M Futures Testnet
- Quantity is in the base asset (e.g., BTC for BTCUSDT)
- LIMIT orders use Good-Till-Cancelled (GTC) time in force
- The testnet account has sufficient balance to place orders

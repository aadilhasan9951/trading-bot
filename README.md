# Trading Bot for Binance Futures Testnet

Small Python bot I threw together for placing orders on Binance Futures Testnet. Does what it says — market, limit, and stop-limit orders via CLI. Nothing fancy, just works.

## Before You Start

1. Head over to https://testnet.binancefuture.com and create an account if you haven't already. It's the testnet, so don't worry about real money.
2. Once logged in, generate an API key and secret from the API Management section. Copy both somewhere safe.
3. Set them as environment variables in your terminal:

```powershell
$env:BINANCE_API_KEY="paste_your_key_here"
$env:BINANCE_API_SECRET="paste_your_secret_here"
```

4. Install the only dependency:

```bash
pip install -r requirements.txt
```

## How to Use

Open a terminal and run:

```bash
python cli.py BTCUSDT BUY MARKET 0.001
python cli.py BTCUSDT SELL LIMIT 0.001 60000
python cli.py BTCUSDT BUY STOP_LIMIT 0.001 51000 50500
```

The pattern is: `python cli.py <symbol> <side> <type> <quantity> [price] [stop_price]`

Price is mandatory for LIMIT and STOP_LIMIT orders. Stop price is only needed for STOP_LIMIT.

## What You'll See

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

If something's wrong (bad input, API error, network timeout), it'll tell you what happened instead of crashing silently.

## Project Structure

```
trading_bot/
  bot/
    client.py          # Talks to Binance API, handles auth & signing
    orders.py          # Decides what to send based on order type
    validators.py      # Checks if your inputs make sense
    logging_config.py  # Sets up logging to file + console
  cli.py               # You interact with this
  logs/
    trading_bot.log    # Gets created automatically when you run the bot
  README.md
  requirements.txt
```

## Things I Assumed

- You're using USDT-M Futures Testnet (not coin-margined or spot)
- Quantity is in the base asset — so for BTCUSDT you type 0.001 (meaning 0.001 BTC)
- Limit orders use Good-Till-Cancelled time-in-force (sits there until filled or you cancel)
- Stop-limit uses Binance's `STOP` order type under the hood

## Why I Didn't Use python-binance

Could've gone with the library but decided to keep it lightweight. Only dependency is `requests` — no bloated third-party SDKs to worry about. HMAC signing is straightforward anyway.

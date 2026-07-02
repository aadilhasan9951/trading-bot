import hashlib
import hmac
import time
import logging
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger("trading_bot.client")

BASE_URL = "https://testnet.binancefuture.com"


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, method: str, endpoint: str, signed: bool = False, **kwargs) -> dict[str, Any]:
        url = f"{BASE_URL}{endpoint}"
        params = kwargs.pop("params", {}) or {}

        if signed:
            params["timestamp"] = int(time.time() * 1000)
            params["recvWindow"] = 60000
            query_string = urlencode(sorted(params.items()))
            signature = self._sign(query_string)
            full_url = f"{url}?{query_string}&signature={signature}"
        else:
            full_url = url

        logger.debug("Request: %s %s", method, full_url)

        try:
            resp = self.session.request(method, full_url, timeout=10)
        except requests.exceptions.Timeout as e:
            logger.error("Request timed out: %s", e)
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s", e)
            raise ConnectionError(f"Failed to connect: {e}")

        logger.debug("Response: %s %s", resp.status_code, resp.text)

        if resp.status_code != 200:
            try:
                body = resp.json()
                msg = body.get("msg", "Unknown error")
                code = body.get("code", -1)
            except Exception:
                msg = resp.text
                code = -1
            logger.error("API error %s: %s", code, msg)
            raise Exception(f"API error ({code}): {msg}")

        return resp.json()

    def place_order(self, **params) -> dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", signed=True, params=params)

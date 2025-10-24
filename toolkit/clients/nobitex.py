"""Module contains Nobitex API client."""

from typing import Any

import requests

from config.base import CURRENCY_SYMBOLS, logger, settings

from .base import BaseClient


class NobitexClient(BaseClient):
    """Nobitex API client."""

    def get_trades(self) -> dict[str, dict[str, Any]]:
        """Get all trades from Nobitex API."""
        currency_urls = [
            self.base_url + settings.get_nobitex_currency_url(symbol)
            for symbol in CURRENCY_SYMBOLS
        ]
        responses = {}
        for key, url in zip(CURRENCY_SYMBOLS, currency_urls):
            try:
                response = requests.get(url)
                response.raise_for_status()
                responses[key] = response.json()
            except requests.RequestException as e:
                logger.error(f"Error fetching {key} trades from nobitex: {e}")
        return responses


def get_nobitex_client() -> NobitexClient:
    """Get Nobitex API client."""
    return NobitexClient(base_url=settings.NOBITEX_GATEWAY)

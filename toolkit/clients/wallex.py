"""Module contains wallex API client."""

from typing import Any

import requests

from config.base import CURRENCY_SYMBOLS, logger, settings

from .base import BaseClient


class WallexClient(BaseClient):
    """Wallex API client."""

    def __init__(self, base_url):
        super().__init__(base_url)
        self.api_key = settings.WALLEX_API_KEY

    def get_trades(self) -> dict[str, dict[str, Any]]:
        """Get all trades from Wallex API."""
        headers = {"x-api-key": self.api_key}
        responses = {}
        for key in CURRENCY_SYMBOLS:
            query_params = {"symbol": key}
            try:
                response = requests.get(
                    self.base_url, headers=headers, params=query_params
                )
                response.raise_for_status()
                responses[key] = response.json()
            except requests.RequestException as e:
                logger.error(f"Error fetching {key} trades from wallex: {e}")
        return responses


def get_wallex_client() -> WallexClient:
    """Get Wallex API client."""
    url = settings.WALLEX_GATEWAY.rstrip("/") + settings.WALLEX_TRADES_ENDPOINT
    return WallexClient(base_url=url)

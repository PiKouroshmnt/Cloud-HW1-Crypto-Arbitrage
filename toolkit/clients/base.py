"""Module contains base clients for the application."""

from abc import ABC, abstractmethod


class BaseClient(ABC):
    """Base client for all API clients."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get_trades(self):
        """Get all trades from the API."""
        pass

"""Module defines recurring tasks for Wallex trading operations."""

from typing import Optional

from src.tasks.utils import format_wallex_trades
from toolkit.clients import get_wallex_client


def run_wallex_trades_retrieval() -> dict[str, dict[str, Optional[float]]]:
    """Run the trade retrieval process for Wallex."""
    client = get_wallex_client()
    response = client.get_trades()
    formatted_trades = format_wallex_trades(response)
    return formatted_trades

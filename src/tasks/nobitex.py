"""Module defines recurring tasks for nobitex trading operations."""

from typing import Optional

from src.tasks.utils import format_nobitex_trades
from toolkit.clients import get_nobitex_client


def run_nobitex_trades_retrieval() -> dict[str, dict[str, Optional[float]]]:
    """Run the trade retrieval process for Nobitex."""
    client = get_nobitex_client()
    response = client.get_trades()
    formatted_trades = format_nobitex_trades(response)
    return formatted_trades

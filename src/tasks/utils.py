"""Module defines utilities for scheduled tasks."""

from typing import Any, Optional


def calculate_profit(buy_price: float, sell_price: float) -> tuple[float, float]:
    """
    Calculate profit from buy and sell prices.

    Parameters
    ----------
    buy_price : float
        The price at which the asset was bought.
    sell_price : float
        The price at which the asset was sold.

    Returns
    -------
    tuple[float, float]
        A tuple containing the profit in absolute terms and the profit percentage.
    """
    profit = sell_price - buy_price
    profit_percentage = (profit / buy_price * 100) if buy_price else 0.0
    return profit, profit_percentage


def format_nobitex_trades(
    nobitex_response: dict[str, Any],
) -> dict[str, dict[str, Optional[float]]]:
    """
    Format Nobitex API response.

    Parameters
    ----------
    nobitex_response : Dict[str, Any]
        The raw response from Nobitex API CLient.

    Returns
    -------
    Dict[str, Dict[str, Optional[float]]]
        A dictionary with currency keys and their latest buy/sell prices.
    """
    formatted_data = {}

    for currency_key, currency_data in nobitex_response.items():
        if currency_data.get("status") != "ok" or not currency_data.get("trades"):
            formatted_data[currency_key] = {
                "latest_buy_price": None,
                "latest_sell_price": None,
            }
            continue

        trades = currency_data["trades"]
        latest_buy_price = None
        latest_sell_price = None

        for trade in trades:
            if trade.get("type") == "buy" and latest_buy_price is None:
                latest_buy_price = float(trade["price"])
            elif trade.get("type") == "sell" and latest_sell_price is None:
                latest_sell_price = float(trade["price"])

            if latest_buy_price is not None and latest_sell_price is not None:
                break

        formatted_data[currency_key] = {
            "latest_buy_price": latest_buy_price,
            "latest_sell_price": latest_sell_price,
        }

    return formatted_data


def format_wallex_trades(
    wallex_response: dict[str, Any],
) -> dict[str, dict[str, Optional[float]]]:
    """
    Format Wallex API response.

    Parameters
    ----------
    wallex_response : dict[str, Any]
        The raw response from Wallex API Client.

    Returns
    -------
    dict[str, dict[str, Optional[float]]]
        A dictionary with currency keys and their latest buy/sell prices.
    """
    formatted_data = {}

    for currency_key, currency_data in wallex_response.items():
        if not currency_data.get("success") or not currency_data.get("result", {}).get(
            "latestTrades"
        ):
            formatted_data[currency_key] = {
                "latest_buy_price": None,
                "latest_sell_price": None,
            }
            continue

        trades = currency_data["result"]["latestTrades"]
        latest_buy_price = None
        latest_sell_price = None

        for trade in trades:
            if trade.get("isBuyOrder") is True and latest_buy_price is None:
                latest_buy_price = float(trade["price"])
            elif trade.get("isBuyOrder") is False and latest_sell_price is None:
                latest_sell_price = float(trade["price"])

            if latest_buy_price is not None and latest_sell_price is not None:
                break

        formatted_data[currency_key] = {
            "latest_buy_price": latest_buy_price,
            "latest_sell_price": latest_sell_price,
        }

    return formatted_data

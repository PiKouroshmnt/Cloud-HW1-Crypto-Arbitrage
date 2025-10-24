"""Module defines base recurring tasks for trading operations."""

from typing import Optional

from config.base import logger, settings
from src.monitoring.metrics import metrics
from toolkit.telegram import get_telegram_client

from .nobitex import run_nobitex_trades_retrieval
from .utils import calculate_profit
from .wallex import run_wallex_trades_retrieval


def _check_and_send_arbitrage_alert(
    currency: str,
    buy_price: Optional[float],
    sell_price: Optional[float],
    direction: str,
    threshold: float,
    telegram_client,
) -> None:
    """
    Check if arbitrage opportunity exists and send alert if profitable.

    Parameters
    ----------
    currency : str
        The currency pair being checked (e.g., 'BTCUSDT')
    buy_price : Optional[float]
        The price to buy at (from one exchange)
    sell_price : Optional[float]
        The price to sell at (from another exchange)
    direction : str
        Direction of the arbitrage (e.g., 'Nobitex→Wallex')
    threshold : float
        Minimum profit percentage threshold to trigger alert
    telegram_client
        Telegram client instance for sending messages
    """
    if buy_price is not None and sell_price is not None and sell_price > buy_price:
        profit, profit_percentage = calculate_profit(buy_price, sell_price)

        if profit_percentage >= threshold:
            logger.info(f"Arbitrage opportunity found for {currency}: {direction}")

            metrics.record_arbitrage_opportunity(currency, direction, profit)

            telegram_client.send_message(
                currency=f"{currency} ({direction})",
                buy_price=buy_price,
                sell_price=sell_price,
                profit_percentage=profit_percentage,
                profit_difference=profit,
            )


def check_for_arbitrage_opportunities() -> None:
    """Check for arbitrage opportunities between Nobitex and Wallex."""
    try:
        nobitex_trades = run_nobitex_trades_retrieval()
        wallex_trades = run_wallex_trades_retrieval()

        if not nobitex_trades or not wallex_trades:
            logger.warning("Failed to retrieve trade data from one or both exchanges")
            return

        metrics.update_latest_prices("nobitex", nobitex_trades)
        metrics.update_latest_prices("wallex", wallex_trades)

        common_currencies = set(nobitex_trades.keys()) & set(wallex_trades.keys())

        if not common_currencies:
            logger.info("No common currencies found between exchanges")
            return

        telegram_client = get_telegram_client()
        threshold = settings.THRESHOLD

        logger.info(
            f"Checking arbitrage opportunities for {len(common_currencies)}"
            f" currencies with threshold {threshold}%"
        )

        for currency in common_currencies:
            nobitex_data = nobitex_trades[currency]
            wallex_data = wallex_trades[currency]

            # Check arbitrage opportunity 1: Buy on Nobitex, Sell on Wallex
            _check_and_send_arbitrage_alert(
                currency=currency,
                buy_price=nobitex_data["latest_buy_price"],
                sell_price=wallex_data["latest_sell_price"],
                direction="Nobitex→Wallex",
                threshold=threshold,
                telegram_client=telegram_client,
            )

            # Check arbitrage opportunity 2: Buy on Wallex, Sell on Nobitex
            _check_and_send_arbitrage_alert(
                currency=currency,
                buy_price=wallex_data["latest_buy_price"],
                sell_price=nobitex_data["latest_sell_price"],
                direction="Wallex→Nobitex",
                threshold=threshold,
                telegram_client=telegram_client,
            )

        metrics.record_arbitrage_check()

        logger.info("Arbitrage check completed successfully")

    except Exception as e:
        logger.error(f"Error during arbitrage check: {e}", exc_info=True)


def run_arbitrage_check() -> None:
    """Run the arbitrage check task."""
    check_for_arbitrage_opportunities()

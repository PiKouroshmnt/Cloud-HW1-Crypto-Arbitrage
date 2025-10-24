"""Module contains Telegram API client."""

from datetime import datetime, timedelta, timezone

import requests

from config.base import logger, settings

from .constants import MESSAGE_TEXT


class TelegramClient:
    """Client for interacting with the Telegram API."""

    def send_message(
        self,
        currency: str,
        buy_price: float,
        sell_price: float,
        profit_percentage: float,
        profit_difference: float,
    ) -> None:
        """Send a message to the Telegram API."""
        utc_now = datetime.now(timezone.utc)
        iran_tz = timezone(timedelta(hours=3, minutes=30))  # UTC+3:30
        iran_time = utc_now.astimezone(iran_tz)

        message = MESSAGE_TEXT.format(
            currency_name=currency,
            time=iran_time.strftime("%Y-%m-%d %H:%M:%S"),
            buy_price=buy_price,
            sell_price=sell_price,
            profit_percentage=profit_percentage,
            profit_difference=profit_difference,
        )
        response = requests.post(
            url=settings.SEND_URL,
            json={
                "chat_id": settings.DM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
            },
        )
        if response.status_code != 200:
            logger.error(f"Failed to send message: {response.text}")


def get_telegram_client() -> TelegramClient:
    """Get Telegram API client."""
    return TelegramClient()

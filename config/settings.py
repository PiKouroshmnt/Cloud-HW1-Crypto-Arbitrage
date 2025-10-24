"""Module contains application settings."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    NOBITEX_GATEWAY: Annotated[str, Field(description="Nobitex API Gateway URL")]
    NOBITEX_TRADES_ENDPOINT: Annotated[
        str, Field(description="Nobitex API Trades Endpoint URL")
    ]

    WALLEX_GATEWAY: Annotated[str, Field(description="Wallex API Gateway URL")]
    WALLEX_TRADES_ENDPOINT: Annotated[
        str, Field(description="Wallex API Trades Endpoint URL")
    ]
    WALLEX_API_KEY: Annotated[str, Field(description="Wallex API Key")]

    THRESHOLD: Annotated[float, Field(description="Arbitrage threshold percentage")]

    BOT_API_TOKEN: Annotated[str, Field(description="Telegram Bot API Token")]
    DM_CHAT_ID: Annotated[int, Field(description="Telegram DM Chat ID")]
    SEND_MESSAGE_URL: Annotated[str, Field(description="Telegram Send Message URL")]

    def get_nobitex_currency_url(self, currency_id: str) -> str:
        """Get Nobitex currency trading URL."""
        return f"{self.NOBITEX_TRADES_ENDPOINT.format(currency_id=currency_id)}"

    @property
    def SEND_URL(self) -> str:
        """Get Telegram Send Message URL."""
        return f"{self.SEND_MESSAGE_URL.format(BOT_API_TOKEN=self.BOT_API_TOKEN)}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

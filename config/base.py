"""Module configures base settings for the application."""

from .consts import CURRENCY_SYMBOLS
from .logging import logger
from .settings import Settings

settings = Settings()

__all__ = ["CURRENCY_SYMBOLS", "logger", "settings"]

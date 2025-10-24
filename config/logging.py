"""Module configures logger for application."""

import sys

from loguru import logger

logger.remove()
logger.add(
    "logs/system_events.log",
    format="Log: {time} - {level} - {message} ",
    level="INFO",
    enqueue=True,
    serialize=True,
)

logger.add(
    sys.stdout,
    format="Log: {time} - {level} - {message} ",
    level="INFO",
    enqueue=True,
)

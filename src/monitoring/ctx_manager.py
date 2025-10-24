"""Module defines context manager for API timing in prometheus."""

import time
from typing import Optional

from .metrics import metrics


class APITimer:
    """Context manager for timing API requests."""

    def __init__(self, exchange: str, currency: str):
        """Initialize timer."""
        self.exchange = exchange
        self.currency = currency
        self.start_time: Optional[float] = None
        self.success = False

    def __enter__(self) -> "APITimer":
        """Start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Stop timing and record metrics."""
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.success = exc_type is None
            metrics.record_api_request(
                self.exchange, self.currency, duration, self.success
            )

    def mark_success(self) -> None:
        """Mark the request as successful."""
        self.success = True

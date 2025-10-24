"""Module for Prometheus metrics collection."""

from typing import Optional

from prometheus_client import Counter, Gauge, Histogram, generate_latest


class ArbitrageMetrics:
    """Singleton class for collecting arbitrage-related metrics."""

    _instance: Optional["ArbitrageMetrics"] = None

    def __new__(cls) -> "ArbitrageMetrics":
        """Create singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_metrics()
        return cls._instance

    def _initialize_metrics(self) -> None:
        """Initialize Prometheus metrics."""
        self.api_request_duration = Histogram(
            "api_request_duration_seconds",
            "Time spent on API requests",
            labelnames=["exchange", "currency"],
        )

        self.api_request_total = Counter(
            "api_requests_total",
            "Total number of API requests",
            labelnames=["exchange", "currency", "status"],
        )

        self.arbitrage_opportunities_total = Counter(
            "arbitrage_opportunities_total",
            "Total number of arbitrage opportunities detected",
            labelnames=["currency", "direction"],
        )

        self.arbitrage_checks_total = Counter(
            "arbitrage_checks_total",
            "Total number of arbitrage checks performed",
        )

        self.arbitrage_detection_rate = Gauge(
            "arbitrage_detection_rate",
            "Rate of arbitrage opportunities detected (opportunities/total_checks)",
            labelnames=["currency", "direction"],
        )

        self.latest_price_difference = Gauge(
            "latest_price_difference",
            "Latest price difference observed for each currency",
            labelnames=["currency", "direction"],
        )

        self.last_successful_check = Gauge(
            "last_successful_arbitrage_check_timestamp",
            "Timestamp of the last successful arbitrage check",
        )

        self._latest_prices: dict[str, dict[str, Optional[float]]] = {}

    def record_api_request(
        self,
        exchange: str,
        currency: str,
        duration: float,
        success: bool,
    ) -> None:
        """Record API request metrics."""
        self.api_request_duration.labels(exchange=exchange, currency=currency).observe(
            duration
        )

        status = "success" if success else "failure"
        self.api_request_total.labels(
            exchange=exchange, currency=currency, status=status
        ).inc()

    def record_arbitrage_opportunity(
        self,
        currency: str,
        direction: str,
        price_difference: float,
    ) -> None:
        """Record arbitrage opportunity detection."""
        self.arbitrage_opportunities_total.labels(
            currency=currency, direction=direction
        ).inc()

        self.latest_price_difference.labels(currency=currency, direction=direction).set(
            price_difference
        )

        self._update_arbitrage_rate(currency, direction)

    def record_arbitrage_check(self) -> None:
        """Record that an arbitrage check was performed."""
        self.arbitrage_checks_total.inc()
        self.last_successful_check.set_to_current_time()

        self._update_all_arbitrage_rates()

    def _update_arbitrage_rate(self, currency: str, direction: str) -> None:
        """Update arbitrage detection rate for specific currency and direction."""
        total_checks = self.arbitrage_checks_total._value._value
        if total_checks > 0:
            try:
                opportunities = self.arbitrage_opportunities_total.labels(
                    currency=currency, direction=direction
                )._value._value
                rate = opportunities / total_checks
                self.arbitrage_detection_rate.labels(
                    currency=currency, direction=direction
                ).set(rate)
            except Exception:
                self.arbitrage_detection_rate.labels(
                    currency=currency, direction=direction
                ).set(0.0)

    def _update_all_arbitrage_rates(self) -> None:
        """Update arbitrage detection rates for all currencies and directions."""
        total_checks = self.arbitrage_checks_total._value._value
        if total_checks > 0:
            for sample in self.arbitrage_opportunities_total.collect()[0].samples:
                currency = sample.labels.get("currency", "")
                direction = sample.labels.get("direction", "")
                if currency and direction:
                    opportunities = sample.value
                    rate = opportunities / total_checks
                    self.arbitrage_detection_rate.labels(
                        currency=currency, direction=direction
                    ).set(rate)

    def update_latest_prices(
        self,
        exchange: str,
        currency_prices: dict[str, dict[str, Optional[float]]],
    ) -> None:
        """Update latest prices and calculate differences."""
        if exchange not in self._latest_prices:
            self._latest_prices[exchange] = {}

        self._latest_prices[exchange] = currency_prices

        if len(self._latest_prices) >= 2:
            exchanges = list(self._latest_prices.keys())
            if len(exchanges) >= 2:
                exchange1, exchange2 = exchanges[0], exchanges[1]
                self._update_price_differences(exchange1, exchange2)

    def _update_price_differences(self, exchange1: str, exchange2: str) -> None:
        """Update price difference gauges for all currencies."""
        exchange1_prices = self._latest_prices.get(exchange1, {})
        exchange2_prices = self._latest_prices.get(exchange2, {})

        common_currencies = set(exchange1_prices.keys()) & set(exchange2_prices.keys())

        for currency in common_currencies:
            e1_data = exchange1_prices[currency]
            e2_data = exchange2_prices[currency]

            # Direction 1: exchange1 -> exchange2
            if (
                e1_data["latest_buy_price"] is not None
                and e2_data["latest_sell_price"] is not None
            ):
                diff = e2_data["latest_sell_price"] - e1_data["latest_buy_price"]
                direction = f"{exchange1}→{exchange2}"
                self.latest_price_difference.labels(
                    currency=currency, direction=direction
                ).set(diff)

            # Direction 2: exchange2 -> exchange1
            if (
                e2_data["latest_buy_price"] is not None
                and e1_data["latest_sell_price"] is not None
            ):
                diff = e1_data["latest_sell_price"] - e2_data["latest_buy_price"]
                direction = f"{exchange2}→{exchange1}"
                self.latest_price_difference.labels(
                    currency=currency, direction=direction
                ).set(diff)

    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        return generate_latest().decode("utf-8")


# Global metrics instance
metrics = ArbitrageMetrics()

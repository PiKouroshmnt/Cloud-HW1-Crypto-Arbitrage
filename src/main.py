"""Module defines main entry point for the application."""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from .lifespan import lifespan
from .monitoring.metrics import metrics

app = FastAPI(
    title="Kourosh's Arbitrage Checker",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "kourosh-arbitrage-checker"}


@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics() -> str:
    """Prometheus metrics endpoint."""
    return metrics.get_metrics()

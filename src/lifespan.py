"""Module for managing application lifespan events."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from src.tasks.base import run_arbitrage_check

scheduler = BackgroundScheduler()
scheduler.add_job(run_arbitrage_check, "interval", seconds=10)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Set application lifespan event manager."""
    scheduler.start()
    yield
    scheduler.shutdown()

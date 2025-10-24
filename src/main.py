"""Module defines main entry point for the application."""

from fastapi import FastAPI

from .lifespan import lifespan

app = FastAPI(
    title="Kourosh's Arbitrage Checker",
    version="1.0.0",
    lifespan=lifespan,
)

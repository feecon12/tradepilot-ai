from fastapi import FastAPI
from app.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="TradePilot AI",
        version="0.1.0",
        description="AI Powered Trading Platform",
    )

    app.include_router(api_router)

    return app
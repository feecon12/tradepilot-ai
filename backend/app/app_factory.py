from fastapi import FastAPI
from app.api.router import api_router
from app.api.routes.instruments import router as instrument_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="TradePilot AI",
        version="0.1.0",
        description="AI Powered Trading Platform",
    )

    app.include_router(api_router)
    app.include_router(
        instrument_router,
        prefix="/api/v1",
    )

    @app.get("/")
    async def health_check():
        return {
            "application": "TradePilot AI",
            "status": "Running",
        }

    return app
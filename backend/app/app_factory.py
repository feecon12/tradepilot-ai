from fastapi import FastAPI

from app.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="TradePilot AI",
        version="1.0.0",
    )

    app.include_router(api_router)

    @app.get("/")
    def root():
        return {"message": "TradePilot AI API"}

    return app
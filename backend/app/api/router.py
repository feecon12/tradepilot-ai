from fastapi import APIRouter

from app.api.routes.instruments import router as instrument_router
from app.api.routes.auth import router as auth_router

from app.api.routes.watchlists import router as watchlist_router

from app.api.routes.portfolios import router as portfolio_router

from app.api.routes.holdings import router as holding_router

from app.api.routes.transactions import router as transaction_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router) 
api_router.include_router(instrument_router)
api_router.include_router(watchlist_router)
api_router.include_router(portfolio_router)
api_router.include_router(holding_router)
api_router.include_router(transaction_router)
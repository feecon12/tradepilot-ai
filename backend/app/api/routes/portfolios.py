from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import (
    get_current_user,
    get_portfolio_service,
)
from app.models import User
from app.schemas import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioResponse,
    PortfolioListResponse,
)
from app.services import PortfolioService


router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)


@router.post(
    "",
    response_model=PortfolioResponse,
)
def create_portfolio(
    data: PortfolioCreate,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return service.create(
            current_user,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=PortfolioListResponse,
)
def get_portfolios(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    return service.get_paginated(
        current_user=current_user,
        page=page,
        size=size,
    )


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def get_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    return service.get_by_id(
        current_user,
        portfolio_id,
    )


@router.put(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: int,
    data: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return service.update(
            current_user,
            portfolio_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    service: PortfolioService = Depends(get_portfolio_service),
):
    service.delete(
        current_user,
        portfolio_id,
    )
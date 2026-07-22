from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import (
    get_current_user,
    get_watchlist_service,
)
from app.models.user import User
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistUpdate,
    WatchlistResponse,
    WatchlistListResponse,
)
from app.services.watchlist_service import WatchlistService

router = APIRouter(
    prefix="/watchlists",
    tags=["Watchlists"],
)


@router.post(
    "",
    response_model=WatchlistResponse,
)
def create_watchlist(
    data: WatchlistCreate,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service),
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
    response_model=WatchlistListResponse,
)
def get_watchlists(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service),
):
    return service.get_paginated(
        current_user=current_user,
        page=page,
        size=size,
    )


@router.get(
    "/{watchlist_id}",
    response_model=WatchlistResponse,
)
def get_watchlist(
    watchlist_id: int,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service),
):
    return service.get_by_id(
        current_user,
        watchlist_id,
    )


@router.put(
    "/{watchlist_id}",
    response_model=WatchlistResponse,
)
def update_watchlist(
    watchlist_id: int,
    data: WatchlistUpdate,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service),
):
    try:
        return service.update(
            current_user,
            watchlist_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{watchlist_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_watchlist(
    watchlist_id: int,
    current_user: User = Depends(get_current_user),
    service: WatchlistService = Depends(get_watchlist_service),
):
    service.delete(
        current_user,
        watchlist_id,
    )
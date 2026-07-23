from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.auth import get_current_user
from app.api.dependencies import get_holding_service
from app.models.user import User

from app.schemas.holding import (
    HoldingCreate,
    HoldingUpdate,
    HoldingResponse,
    HoldingListResponse,
)

from app.services.holding_service import HoldingService


router = APIRouter(
    prefix="/holdings",
    tags=["Holdings"],
)


@router.post(
    "",
    response_model=HoldingResponse,
)
def create_holding(
    data: HoldingCreate,
    current_user: User = Depends(get_current_user),
    service: HoldingService = Depends(get_holding_service),
):
    try:
        return service.create(
            current_user=current_user,
            data=data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "",
    response_model=HoldingListResponse,
)
def get_holdings(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: HoldingService = Depends(get_holding_service),
):
    return service.get_paginated(
        current_user=current_user,
        page=page,
        size=size,
    )


@router.get(
    "/{holding_id}",
    response_model=HoldingResponse,
)
def get_holding(
    holding_id: int,
    current_user: User = Depends(get_current_user),
    service: HoldingService = Depends(get_holding_service),
):
    return service.get_by_id(
        current_user=current_user,
        holding_id=holding_id,
    )


@router.put(
    "/{holding_id}",
    response_model=HoldingResponse,
)
def update_holding(
    holding_id: int,
    data: HoldingUpdate,
    current_user: User = Depends(get_current_user),
    service: HoldingService = Depends(get_holding_service),
):
    return service.update(
        current_user=current_user,
        holding_id=holding_id,
        data=data,
    )


@router.delete(
    "/{holding_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_holding(
    holding_id: int,
    current_user: User = Depends(get_current_user),
    service: HoldingService = Depends(get_holding_service),
):
    service.delete(
        current_user=current_user,
        holding_id=holding_id,
    )
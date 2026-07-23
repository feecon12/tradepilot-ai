from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.auth import get_current_user
from app.api.dependencies import get_transaction_service

from app.models.user import User

from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
    TransactionListResponse,
)

from app.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.post(
    "",
    response_model=TransactionResponse,
)
def create_transaction(
    data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
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
    response_model=TransactionListResponse,
)
def get_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.get_paginated(
        current_user=current_user,
        page=page,
        size=size,
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.get_by_id(
        current_user=current_user,
        transaction_id=transaction_id,
    )


@router.put(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return service.update(
        current_user=current_user,
        transaction_id=transaction_id,
        data=data,
    )


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    service.delete(
        current_user=current_user,
        transaction_id=transaction_id,
    )
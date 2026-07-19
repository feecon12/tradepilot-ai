from fastapi import APIRouter, Depends, HTTPException
from app.schemas.instrument import (
    InstrumentCreate,
    InstrumentResponse,
    InstrumentUpdate,
    InstrumentListResponse
)
from app.services.instrument_service import InstrumentService
from fastapi  import status, Query
from app.api.dependencies import get_instrument_service

from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"],
)

@router.post(
    "",
    response_model=InstrumentResponse,
)
def create_instrument(
    data: InstrumentCreate,
    current_user: User = Depends(get_current_user),
    service: InstrumentService=Depends(get_instrument_service),
):
    try:
        return service.create(data)
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "",
    response_model=InstrumentListResponse,
)
def get_instruments(
    page: int=Query(1, ge=1),
    size: int=Query(10,ge=1, le=100),
    search: str | None = None,
    exchange: str | None = None,
    instrument_type: str | None = None,
    is_active: bool | None = None,
    current_user: User = Depends(get_current_user),
    service: InstrumentService = Depends(get_instrument_service),
): 
    return service.get_paginated(
        page=page,
        size=size,
        search=search,
        exchange=exchange,
        instrument_type=instrument_type,
        is_active=is_active,
    )

@router.get(
    "/{instrument_id}",
    response_model=InstrumentResponse
)
def get_instrument_by_id(
    instrument_id:int,
    current_user: User = Depends(get_current_user),
    service: InstrumentService = Depends(get_instrument_service)  
):
    return service.get_by_id(instrument_id)

@router.put(
    "/{instrument_id}",
    response_model=InstrumentResponse,
)
def update_instrument(
    instrument_id: int,
    data:InstrumentUpdate,
    current_user: User = Depends(get_current_user),
    service: InstrumentService = Depends(get_instrument_service)  


):
    return service.update(instrument_id,data)

@router.delete(
    "/{instrument_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_instrument(
    instrument_id: int,
    current_user: User = Depends(get_current_user),
    service: InstrumentService = Depends(get_instrument_service)  

):
    service.delete(instrument_id)

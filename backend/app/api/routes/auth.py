from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router =  APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try: 
        return service.register(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
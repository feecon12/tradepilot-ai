from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_service
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service

from fastapi.security import OAuth2PasswordRequestForm

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

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService= Depends(get_auth_service),
):
    return service.login(form_data)

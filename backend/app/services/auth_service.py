from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest

class AuthService:
    def __init__(self, repository:UserRepository):
        self.repository=repository
    
    def login(self, data: LoginRequest):
        user = self.repository.get_by_email(data.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        if not verify_password(
            data.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        
        access_token=create_access_token(
            data={
                "sub":user.email,
            }
        )

        return {
            "access_token":access_token,
            "token_type":"bearer"
        }
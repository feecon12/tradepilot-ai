from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import oauth2_scheme
from app.core.security import decode_access_token
from app.db.database import get_db
from app.repositories.user_repository import UserRepository

def get_current_user(
        token: str= Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> User:
    
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    repository=UserRepository(db)

    user=repository.get_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

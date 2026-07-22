from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.models.user import User

from app.db.database import get_db
from app.repositories.instrument_repository import InstrumentRepository
from app.services.instrument_service import InstrumentService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

from app.services.auth_service import AuthService

from app.repositories.watchlist_repository import WatchlistRepository
from app.services.watchlist_service import WatchlistService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session= Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    email=payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    repository = UserRepository(db)

    user = repository.get_by_email(email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

def get_instrument_service(
        db: Session = Depends(get_db),
) -> InstrumentService:
    repository = InstrumentRepository(db)
    return InstrumentService(repository)

def get_user_service(db: Session = Depends(get_db)):
    repository = UserRepository(db)
    return UserService(repository)

def get_auth_service(
        db: Session = Depends(get_db),
):
    repository=UserRepository(db)
    return AuthService(repository)

def get_watchlist_service(
    db: Session = Depends(get_db),
) -> WatchlistService:

    repository = WatchlistRepository(db)

    return WatchlistService(repository)
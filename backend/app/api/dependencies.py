from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.instrument_repository import InstrumentRepository
from app.services.instrument_service import InstrumentService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

from app.services.auth_service import AuthService

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
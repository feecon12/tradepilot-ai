from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.instrument_repository import InstrumentRepository
from app.services.instrument_service import InstrumentService

def get_instrument_service(
        db: Session = Depends(get_db),
) -> InstrumentService:
    repository = InstrumentRepository(db)
    return InstrumentService(repository)
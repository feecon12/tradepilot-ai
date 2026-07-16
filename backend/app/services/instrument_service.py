from app.models.instrument import Instrument
from app.repositories.instrument_repository import InstrumentRepository
from app.schemas.instrument import InstrumentCreate, InstrumentUpdate
from fastapi import HTTPException
import math
class InstrumentService:
    
    def __init__(self, repository: InstrumentRepository):
        self.repository = repository

    def create(self, data: InstrumentCreate) -> Instrument:
        existing = self.repository.get_by_symbol(data.symbol.upper())

        if existing:
            raise ValueError("Instrument already exists.")
        
        instrument = Instrument(
            symbol=data.symbol.upper(),
            exchange=data.exchange.upper(),
            instrument_type=data.instrument_type.upper()
        )

        return self.repository.create(instrument)
    
    def get_all(self):
        return self.repository.get_all()
    

    def get_by_id(self, instrument_id: int):
        instrument = self.repository.get_by_id(instrument_id)

        if not instrument:
            raise HTTPException(
                status_code=404,
                detail="Instrument not found",
            )

        return instrument
    
    def update(self, instrument_id: int, data:InstrumentUpdate):
        instrument=self.repository.get_by_id(instrument_id)

        if not instrument:
            raise HTTPException(
                status_code=404,
                detail="Instrumnent not found",
            )
        instrument.exchange=data.exchange.upper()
        instrument.instrument_type=data.instrument_type.upper()
        instrument.is_active=data.is_active

        return self.repository.update(instrument)
    
    def delete(self, instrument_id: int):
        instrument=self.repository.get_by_id(instrument_id)

        if not instrument:
            raise HTTPException(
                status_code=404,
                detail="Instrument not found",
            )
        self.repository.delete(instrument)

    def get_paginated(
        self, 
        page:int, 
        size:int,
        search: str | None = None,
        exchange: str | None = None,
        instrument_type: str | None = None,
        is_active: bool | None = None,
    ):

        items, total = self.repository.get_paginated(
            page=page, 
            size=size,
            search=search,
            exchange=exchange,
            instrument_type=instrument_type,
            is_active=is_active
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": math.ceil(total / size) if total else 0,
        }
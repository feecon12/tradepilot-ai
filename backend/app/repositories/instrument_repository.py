from sqlalchemy.orm import Session
from app.models.instrument import Instrument

class InstrumentRepository:
    def __init__(self,db:Session):
        self.db = db

    def create(self, instrument: Instrument) -> Instrument:
        self.db.add(instrument)
        self.db.commit()
        self.db.refresh(instrument)
        return instrument
    
    def get_all(self) -> list[Instrument]:
        return self.db.query(Instrument).all()
    
    def get_by_id(self, instrument_id: int) -> Instrument | None:
        return (
            self.db.query(Instrument)
            .filter(Instrument.id == instrument_id)
            .first()
        )
    
    def get_by_symbol(self, symbol:str) -> Instrument | None:
        return (
            self.db.query(Instrument)
            .filter(Instrument.symbol == symbol)
            .first()
        )
    
    def update(self, instrument: Instrument) -> Instrument:
        self.db.commit()
        self.db.refresh(instrument)
        return instrument

    def delete(self, instrument:Instrument) -> None:
        self.db.delete(instrument)
        self.db.commit()

    def get_paginated(
            self, 
            page: int, 
            size: int, 
            search: str | None =  None, 
            exchange: str | None = None, 
            instrument_type: str | None=None, 
            is_active: bool | None=None
        ):
        query = self.db.query(Instrument)

        if search:
            query = query.filter(
                Instrument.symbol.ilike(f"%{search}%")
            )

        if exchange:
            query =  query.filter(
                Instrument.exchange==exchange.upper()
            )

        if instrument_type:
            query=query.filter(
                Instrument.instrument_type==instrument_type.upper()
            )
        
        if is_active is not None:
            query=query.filter(
                Instrument.is_active==is_active
            )
        
        total = query.count()

        items = (
            query
            .offset((page-1)*size)
            .limit(size)
            .all()
        )
        return items, total
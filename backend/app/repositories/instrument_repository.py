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

    def get_paginated(self, page: int, size: int):
        total = self.db.query(Instrument).count()

        items = (
            self.db.query(Instrument)
            .offset((page-1)*size)
            .limit(size)
            .all()
        )
        return items, total
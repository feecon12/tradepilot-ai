from pydantic import BaseModel
from typing import Optional

class InstrumentCreate(BaseModel):
    symbol: str
    exchange: str
    instrument_type: str

class InstrumentResponse(BaseModel):
    id: int
    symbol: str
    exchange: str
    instrument_type: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class InstrumentUpdate(BaseModel):
    symbol: Optional[str] = None
    exchange: Optional[str] = None
    instrument_type: Optional[str] = None
    is_active: Optional[bool] = None

class InstrumentListResponse(BaseModel):
    items: list[InstrumentResponse]
    total: int
    page: int
    size: int
    pages: int

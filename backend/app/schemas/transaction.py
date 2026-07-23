from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    portfolio_id: int
    instrument_id: int
    transaction_type: str
    quantity: float
    price: float


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    quantity: float | None = None
    price: float | None = None


class TransactionResponse(TransactionBase):
    id: int
    transaction_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    page: int
    size: int
    pages: int
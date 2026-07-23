from pydantic import BaseModel, ConfigDict


class HoldingBase(BaseModel):
    portfolio_id: int
    instrument_id: int
    quantity: float
    average_price: float


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    quantity: float | None = None
    average_price: float | None = None


class HoldingResponse(HoldingBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class HoldingListResponse(BaseModel):
    items: list[HoldingResponse]
    total: int
    page: int
    size: int
    pages: int
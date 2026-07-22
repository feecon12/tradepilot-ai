from pydantic import BaseModel, ConfigDict


class PortfolioBase(BaseModel):
    name: str
    description: str | None = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(PortfolioBase):
    pass


class PortfolioResponse(PortfolioBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class PortfolioListResponse(BaseModel):
    items: list[PortfolioResponse]
    total: int
    page: int
    size: int
    pages: int
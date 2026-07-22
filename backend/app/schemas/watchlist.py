from pydantic import BaseModel


class WatchlistCreate(BaseModel):
    name: str


class WatchlistUpdate(BaseModel):
    name: str


class WatchlistResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class WatchlistListResponse(BaseModel):
    items: list[WatchlistResponse]
    total: int
    page: int
    size: int
    pages: int
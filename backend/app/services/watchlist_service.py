import math

from fastapi import HTTPException

from app.models.user import User
from app.models.watchlist import Watchlist
from app.repositories.watchlist_repository import WatchlistRepository
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistUpdate,
)


class WatchlistService:

    def __init__(self, repository: WatchlistRepository):
        self.repository = repository

    def create(
        self,
        current_user: User,
        data: WatchlistCreate,
    ) -> Watchlist:

        existing = self.repository.get_by_name(
            data.name,
            current_user.id,
        )

        if existing:
            raise ValueError(
                "Watchlist already exists."
            )

        watchlist = Watchlist(
            name=data.name,
            user_id=current_user.id,
        )

        return self.repository.create(watchlist)

    def get_by_id(
        self,
        current_user: User,
        watchlist_id: int,
    ):

        watchlist = self.repository.get_by_id(
            watchlist_id,
            current_user.id,
        )

        if not watchlist:
            raise HTTPException(
                status_code=404,
                detail="Watchlist not found",
            )

        return watchlist

    def update(
        self,
        current_user: User,
        watchlist_id: int,
        data: WatchlistUpdate,
    ):

        watchlist = self.repository.get_by_id(
            watchlist_id,
            current_user.id,
        )

        if not watchlist:
            raise HTTPException(
                status_code=404,
                detail="Watchlist not found",
            )

        duplicate = self.repository.get_by_name(
            data.name,
            current_user.id,
        )

        if duplicate and duplicate.id != watchlist.id:
            raise ValueError(
                "Watchlist already exists."
            )

        watchlist.name = data.name

        return self.repository.update(watchlist)

    def delete(
        self,
        current_user: User,
        watchlist_id: int,
    ):

        watchlist = self.repository.get_by_id(
            watchlist_id,
            current_user.id,
        )

        if not watchlist:
            raise HTTPException(
                status_code=404,
                detail="Watchlist not found",
            )

        self.repository.delete(watchlist)

    def get_paginated(
        self,
        current_user: User,
        page: int,
        size: int,
    ):

        items, total = self.repository.get_paginated(
            user_id=current_user.id,
            page=page,
            size=size,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": math.ceil(total / size) if total else 0,
        }
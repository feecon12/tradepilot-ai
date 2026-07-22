from sqlalchemy.orm import Session

from app.models.watchlist import Watchlist

class WatchlistRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        watchlist: Watchlist,
    ) -> Watchlist:
        self.db.add(watchlist)
        self.db.commit()
        self.db.refresh(watchlist)
        return watchlist

    def get_by_id(
        self,
        watchlist_id: int,
        user_id: int,
    ) -> Watchlist | None:
        return (
            self.db.query(Watchlist)
            .filter(
                Watchlist.id == watchlist_id,
                Watchlist.user_id == user_id,
            )
            .first()
        )

    def get_by_name(
        self,
        name: str,
        user_id: int,
    ) -> Watchlist | None:
        return (
            self.db.query(Watchlist)
            .filter(
                Watchlist.name == name,
                Watchlist.user_id == user_id,
            )
            .first()
        )

    def update(
        self,
        watchlist: Watchlist,
    ) -> Watchlist:
        self.db.commit()
        self.db.refresh(watchlist)
        return watchlist

    def delete(
        self,
        watchlist: Watchlist,
    ) -> None:
        self.db.delete(watchlist)
        self.db.commit()

    def get_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ):
        query = (
            self.db.query(Watchlist)
            .filter(
                Watchlist.user_id == user_id
            )
        )

        total = query.count()

        items = (
            query
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return items, total
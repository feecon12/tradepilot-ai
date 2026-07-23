from sqlalchemy.orm import Session

from app.models.holding import Holding
from app.models.portfolio import Portfolio


class HoldingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, holding: Holding) -> Holding:
        self.db.add(holding)
        self.db.commit()
        self.db.refresh(holding)
        return holding

    def get_all(self, user_id: int):
        return (
            self.db.query(Holding)
            .join(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .all()
        )

    def get_by_id(
        self,
        holding_id: int,
        user_id: int,
    ) -> Holding | None:
        return (
            self.db.query(Holding)
            .join(Portfolio)
            .filter(
                Holding.id == holding_id,
                Portfolio.user_id == user_id,
            )
            .first()
        )

    def update(
        self,
        holding: Holding,
    ) -> Holding:
        self.db.commit()
        self.db.refresh(holding)
        return holding

    def delete(
        self,
        holding: Holding,
    ) -> None:
        self.db.delete(holding)
        self.db.commit()

    def get_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ):
        query = (
            self.db.query(Holding)
            .join(Portfolio)
            .filter(
                Portfolio.user_id == user_id
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

    def get_by_portfolio_and_instrument(
        self,
        user_id: int,
        portfolio_id: int,
        instrument_id: int,
    ) -> Holding | None:

        return (
            self.db.query(Holding)
            .join(Portfolio)
            .filter(
                Portfolio.user_id == user_id,
                Holding.portfolio_id == portfolio_id,
                Holding.instrument_id == instrument_id,
            )
            .first()
        )

    def add(
    self,
    holding: Holding,
    ):
        self.db.add(holding)
from sqlalchemy.orm import Session

from app.models import Portfolio


class PortfolioRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        portfolio: Portfolio,
    ) -> Portfolio:
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def get_by_id(
        self,
        portfolio_id: int,
        user_id: int,
    ) -> Portfolio | None:
        return (
            self.db.query(Portfolio)
            .filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id,
            )
            .first()
        )

    def get_by_name(
        self,
        name: str,
        user_id: int,
    ) -> Portfolio | None:
        return (
            self.db.query(Portfolio)
            .filter(
                Portfolio.name == name,
                Portfolio.user_id == user_id,
            )
            .first()
        )

    def get_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ):
        query = (
            self.db.query(Portfolio)
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

    def update(
        self,
        portfolio: Portfolio,
    ) -> Portfolio:
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def delete(
        self,
        portfolio: Portfolio,
    ) -> None:
        self.db.delete(portfolio)
        self.db.commit()
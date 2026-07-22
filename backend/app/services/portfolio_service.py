import math

from fastapi import HTTPException

from app.models import Portfolio, User
from app.repositories import PortfolioRepository
from app.schemas import (
    PortfolioCreate,
    PortfolioUpdate,
)


class PortfolioService:

    def __init__(
        self,
        repository: PortfolioRepository,
    ):
        self.repository = repository

    def create(
        self,
        current_user: User,
        data: PortfolioCreate,
    ) -> Portfolio:

        existing = self.repository.get_by_name(
            data.name,
            current_user.id,
        )

        if existing:
            raise ValueError(
                "Portfolio already exists."
            )

        portfolio = Portfolio(
            name=data.name,
            description=data.description,
            user_id=current_user.id,
        )

        return self.repository.create(portfolio)

    def get_by_id(
        self,
        current_user: User,
        portfolio_id: int,
    ) -> Portfolio:

        portfolio = self.repository.get_by_id(
            portfolio_id,
            current_user.id,
        )

        if not portfolio:
            raise HTTPException(
                status_code=404,
                detail="Portfolio not found",
            )

        return portfolio

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

    def update(
        self,
        current_user: User,
        portfolio_id: int,
        data: PortfolioUpdate,
    ) -> Portfolio:

        portfolio = self.repository.get_by_id(
            portfolio_id,
            current_user.id,
        )

        if not portfolio:
            raise HTTPException(
                status_code=404,
                detail="Portfolio not found",
            )

        duplicate = self.repository.get_by_name(
            data.name,
            current_user.id,
        )

        if duplicate and duplicate.id != portfolio.id:
            raise ValueError(
                "Portfolio already exists."
            )

        portfolio.name = data.name
        portfolio.description = data.description

        return self.repository.update(portfolio)

    def delete(
        self,
        current_user: User,
        portfolio_id: int,
    ) -> None:

        portfolio = self.repository.get_by_id(
            portfolio_id,
            current_user.id,
        )

        if not portfolio:
            raise HTTPException(
                status_code=404,
                detail="Portfolio not found",
            )

        self.repository.delete(portfolio)
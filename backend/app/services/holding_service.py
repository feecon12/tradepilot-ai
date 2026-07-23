import math

from fastapi import HTTPException

from app.models.holding import Holding
from app.models.user import User
from app.repositories.holding_repository import HoldingRepository
from app.schemas.holding import (
    HoldingCreate,
    HoldingUpdate,
)


class HoldingService:

    def __init__(
        self,
        repository: HoldingRepository,
    ):
        self.repository = repository

    def create(
        self,
        current_user: User,
        data: HoldingCreate,
    ) -> Holding:

        holding = Holding(
            portfolio_id=data.portfolio_id,
            instrument_id=data.instrument_id,
            quantity=data.quantity,
            average_price=data.average_price,
        )

        return self.repository.create(holding)

    def get_all(
        self,
        current_user: User,
    ):
        return self.repository.get_all(current_user.id)

    def get_by_id(
        self,
        current_user: User,
        holding_id: int,
    ):

        holding = self.repository.get_by_id(
            holding_id,
            current_user.id,
        )

        if not holding:
            raise HTTPException(
                status_code=404,
                detail="Holding not found",
            )

        return holding

    def update(
        self,
        current_user: User,
        holding_id: int,
        data: HoldingUpdate,
    ):

        holding = self.repository.get_by_id(
            holding_id,
            current_user.id,
        )

        if not holding:
            raise HTTPException(
                status_code=404,
                detail="Holding not found",
            )

        if data.quantity is not None:
            holding.quantity = data.quantity

        if data.average_price is not None:
            holding.average_price = data.average_price

        return self.repository.update(holding)

    def delete(
        self,
        current_user: User,
        holding_id: int,
    ):

        holding = self.repository.get_by_id(
            holding_id,
            current_user.id,
        )

        if not holding:
            raise HTTPException(
                status_code=404,
                detail="Holding not found",
            )

        self.repository.delete(holding)

    def get_paginated(
        self,
        current_user: User,
        page: int,
        size: int,
    ):

        items, total = self.repository.get_paginated(
            current_user.id,
            page,
            size,
        )

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": math.ceil(total / size) if total else 0,
        }
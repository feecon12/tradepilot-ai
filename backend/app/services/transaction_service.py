import math

from fastapi import HTTPException

from app.models.transaction import Transaction
from app.models.holding import Holding
from app.models.user import User

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.holding_repository import HoldingRepository

from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
)


class TransactionService:

    def __init__(
        self,
        transaction_repository: TransactionRepository,
        holding_repository: HoldingRepository,
    ):
        self.transaction_repository = transaction_repository
        self.holding_repository = holding_repository

    def create(
        self,
        current_user: User,
        data: TransactionCreate,
    ):

        transaction = Transaction(
            portfolio_id=data.portfolio_id,
            instrument_id=data.instrument_id,
            transaction_type=data.transaction_type.upper(),
            quantity=data.quantity,
            price=data.price,
        )

        self.transaction_repository.create(transaction)

        holding = self.holding_repository.get_by_portfolio_and_instrument(
            user_id=current_user.id,
            portfolio_id=data.portfolio_id,
            instrument_id=data.instrument_id,
        )

        if holding is None:

            holding = Holding(
                portfolio_id=data.portfolio_id,
                instrument_id=data.instrument_id,
                quantity=data.quantity,
                average_price=data.price,
            )

            self.holding_repository.add(holding)

        else:

            total_cost = (
                holding.quantity * holding.average_price
            ) + (
                data.quantity * data.price
            )

            new_quantity = (
                holding.quantity + data.quantity
            )

            holding.quantity = new_quantity

            holding.average_price = (
                total_cost / new_quantity
            )

        self.transaction_repository.commit()

        self.transaction_repository.refresh(transaction)

        return transaction

    def get_by_id(
        self,
        current_user: User,
        transaction_id: int,
    ):

        transaction = self.transaction_repository.get_by_id(
            transaction_id,
            current_user.id,
        )

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found",
            )

        return transaction

    def get_paginated(
        self,
        current_user: User,
        page: int,
        size: int,
    ):

        items, total = self.transaction_repository.get_paginated(
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

    def update(
        self,
        current_user: User,
        transaction_id: int,
        data: TransactionUpdate,
    ):

        transaction = self.get_by_id(
            current_user,
            transaction_id,
        )

        if data.quantity is not None:
            transaction.quantity = data.quantity

        if data.price is not None:
            transaction.price = data.price

        return self.transaction_repository.update(transaction)

    def delete(
        self,
        current_user: User,
        transaction_id: int,
    ):

        transaction = self.get_by_id(
            current_user,
            transaction_id,
        )

        self.transaction_repository.delete(transaction)
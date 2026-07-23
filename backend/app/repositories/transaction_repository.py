from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.portfolio import Portfolio


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        transaction: Transaction,
    ) -> Transaction:

        self.db.add(transaction)
        self.db.flush()

        return transaction

    def get_by_id(
        self,
        transaction_id: int,
        user_id: int,
    ) -> Transaction | None:

        return (
            self.db.query(Transaction)
            .join(Portfolio)
            .filter(
                Transaction.id == transaction_id,
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
            self.db.query(Transaction)
            .join(Portfolio)
            .filter(
                Portfolio.user_id == user_id,
            )
            .order_by(
                Transaction.transaction_date.desc()
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
        transaction: Transaction,
    ):

        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def delete(
        self,
        transaction: Transaction,
    ):

        self.db.delete(transaction)
        self.db.commit()\

    def commit(self):
        self.db.commit()


    def rollback(self):
        self.db.rollback()

    def refresh(
        self,
        transaction: Transaction,
    ):

        self.db.refresh(transaction)    
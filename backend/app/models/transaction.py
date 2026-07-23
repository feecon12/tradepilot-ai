from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id"),
        nullable=False,
    )

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id"),
        nullable=False,
    )

    transaction_type: Mapped[str] = mapped_column(
        String(10),
    )

    quantity: Mapped[float] = mapped_column(
        Float,
    )

    price: Mapped[float] = mapped_column(
        Float,
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="transactions",
    )

    instrument: Mapped["Instrument"] = relationship(
        back_populates="transactions",
    )
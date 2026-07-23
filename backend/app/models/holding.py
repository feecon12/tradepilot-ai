from sqlalchemy import ForeignKey, Float

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class Holding(Base):
    __tablename__ = "holdings"

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

    quantity: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    average_price: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="holdings",
    )

    instrument: Mapped["Instrument"] = relationship(
        back_populates="holdings",
    )
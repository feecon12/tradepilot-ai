from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("Users.id"),
    )

    user: Mapped["User"] = relationship(
        back_populates="portfolios",
    )

    holdings: Mapped[list["Holding"]] = relationship(
    back_populates="portfolio",
    cascade="all, delete-orphan",
    )

    transactions: Mapped[list["Transaction"]] = relationship(
    back_populates="portfolio",
    cascade="all, delete-orphan",
    )
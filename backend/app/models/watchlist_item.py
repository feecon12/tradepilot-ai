from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    watchlist_id: Mapped[int] = mapped_column(
        ForeignKey("watchlists.id"),
        nullable=False,
    )

    instrument_id: Mapped[int] = mapped_column(
        ForeignKey("instruments.id"),
        nullable=False,
    )

    watchlist: Mapped["Watchlist"] = relationship(
        back_populates="items",
    )

    instrument: Mapped["Instrument"] = relationship(
        back_populates="watchlist_items",
    )
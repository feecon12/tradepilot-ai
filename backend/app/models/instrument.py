from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)

    symbol: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )

    exchange: Mapped[str] = mapped_column(
        String(20),
    )

    instrument_type: Mapped[str] = mapped_column(
        String(20),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
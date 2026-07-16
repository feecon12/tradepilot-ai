
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import Boolean, String
from app.db.base import Base

class User(Base):
    __tablename__="Users"

    id: Mapped[int]=mapped_column(primary_key=True)

    username: Mapped[str]= mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    hashed_password: Mapped[str]=mapped_column(
        String(255),
    )

    is_active: Mapped[bool]=mapped_column(
        Boolean,
        default=True
    )
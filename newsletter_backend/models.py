from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import ModelBase


class ModelUser(ModelBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    email_verified: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )

    tokens: Mapped["ModelUserTokens"] = relationship(back_populates="user")


class ModelUserTokens(ModelBase):
    __tablename__ = "user_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), unique=True)
    session_token: Mapped[str]
    session_expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    refresh_token: Mapped[str]
    refresh_expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["ModelUser"] = relationship(back_populates="tokens")

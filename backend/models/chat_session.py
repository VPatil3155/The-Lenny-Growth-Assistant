"""Chat session persistence model.

This model only defines the database record; chat behavior belongs elsewhere.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ChatSession(Base):
    """A durable container for a future conversation."""

    __tablename__ = "chat_sessions"
    __table_args__ = (
        Index("ix_chat_sessions_created_at", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )

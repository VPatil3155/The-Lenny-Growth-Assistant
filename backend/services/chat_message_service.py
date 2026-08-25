"""Database operations for chat messages."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chat_message import ChatMessage


def create_message(
    db: Session, session_id: UUID, role: str, content: str
) -> ChatMessage:
    """Create and persist a message in a chat session."""

    message = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(db: Session, session_id: UUID) -> list[ChatMessage]:
    """Return a session's messages in chronological order."""

    statement = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    return list(db.scalars(statement).all())

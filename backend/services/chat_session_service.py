"""Database operations for chat sessions."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chat_session import ChatSession


DEFAULT_SESSION_TITLE = "Untitled Session"


def create_session(db: Session, title: str | None) -> ChatSession:
    """Create and persist a chat session."""

    session_title = title.strip() if title and title.strip() else DEFAULT_SESSION_TITLE
    chat_session = ChatSession(title=session_title)
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session


def get_all_sessions(db: Session) -> list[ChatSession]:
    """Return all chat sessions, newest first."""

    statement = select(ChatSession).order_by(ChatSession.created_at.desc())
    return list(db.scalars(statement).all())


def get_session(db: Session, session_id: UUID) -> ChatSession | None:
    """Return a chat session by ID when it exists."""

    return db.get(ChatSession, session_id)


def delete_session(db: Session, session_id: UUID) -> bool:
    """Delete a chat session and report whether it was found."""

    chat_session = get_session(db, session_id)
    if chat_session is None:
        return False

    db.delete(chat_session)
    db.commit()
    return True

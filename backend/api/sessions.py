"""HTTP endpoints for chat session CRUD."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from schemas.chat_session import CreateSessionRequest, SessionResponse, UpdateSessionRequest
from services.chat_session_service import (
    create_session,
    delete_session,
    get_all_sessions,
    get_session,
    update_session,
)


router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_chat_session(
    payload: CreateSessionRequest,
    db: Session = Depends(get_db),
) -> SessionResponse:
    """Create a chat session."""

    return create_session(db, payload.title)


@router.get("", response_model=list[SessionResponse])
def list_chat_sessions(db: Session = Depends(get_db)) -> list[SessionResponse]:
    """List all chat sessions."""

    return get_all_sessions(db)


@router.get("/{session_id}", response_model=SessionResponse)
def get_chat_session(
    session_id: UUID,
    db: Session = Depends(get_db),
) -> SessionResponse:
    """Fetch one chat session."""

    chat_session = get_session(db, session_id)
    if chat_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )
    return chat_session


@router.patch("/{session_id}", response_model=SessionResponse)
def update_chat_session(
    session_id: UUID,
    payload: UpdateSessionRequest,
    db: Session = Depends(get_db),
) -> SessionResponse:
    """Update a chat session's title."""

    updated = update_session(db, session_id, payload.title)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )
    return updated


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat_session(
    session_id: UUID,
    db: Session = Depends(get_db),
) -> Response:
    """Delete one chat session."""

    if not delete_session(db, session_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

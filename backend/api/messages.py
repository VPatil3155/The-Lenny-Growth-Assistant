"""HTTP endpoints for chat message persistence."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from schemas.chat_message import ChatTurnResponse, CreateMessageRequest, MessageResponse
from services.chat_message_service import get_messages
from services.chat_session_service import get_session
from services.chat_orchestrator import (
    ChatOrchestrator,
    LLMProviderError,
    SessionNotFoundError,
)


router = APIRouter(prefix="/sessions", tags=["messages"])


@router.post(
    "/{session_id}/messages",
    response_model=ChatTurnResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_message(
    session_id: UUID,
    payload: CreateMessageRequest,
    db: Session = Depends(get_db),
) -> ChatTurnResponse:
    """Send a user message and return the generated, persisted assistant reply."""

    try:
        user_message, assistant_message, updated_session = ChatOrchestrator(db).create_response(
            session_id, payload.content
        )
    except SessionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    except LLMProviderError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate an assistant response.",
        )

    return ChatTurnResponse(
        user_message=user_message,
        assistant_message=assistant_message,
        session=updated_session,
    )


@router.get("/{session_id}/messages", response_model=list[MessageResponse])
def list_chat_messages(
    session_id: UUID,
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    """List an existing chat session's messages chronologically."""

    if get_session(db, session_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    return get_messages(db, session_id)

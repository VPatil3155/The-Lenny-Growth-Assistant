"""Request and response schemas for chat messages."""

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from schemas.chat_session import SessionResponse


class CreateMessageRequest(BaseModel):
    """Payload used to send a user message to an existing chat session."""

    content: str = Field(min_length=1, max_length=10000)
    role: Literal["user"] = "user"


class MessageResponse(BaseModel):
    """Public representation of a chat message."""

    id: UUID
    session_id: UUID
    role: Literal["user", "assistant", "system"]
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatTurnResponse(BaseModel):
    """The persisted user message and generated assistant response."""

    user_message: MessageResponse
    assistant_message: MessageResponse
    session: SessionResponse | None = None

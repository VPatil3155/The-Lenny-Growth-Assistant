"""Request and response schemas for chat sessions."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateSessionRequest(BaseModel):
    """Payload used to create a chat session."""

    title: str | None = Field(default=None, max_length=255)


class UpdateSessionRequest(BaseModel):
    """Payload used to update a chat session."""

    title: str = Field(min_length=1, max_length=255)


class SessionResponse(BaseModel):
    """Public representation of a chat session."""

    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

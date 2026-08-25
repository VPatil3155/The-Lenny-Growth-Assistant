"""Schema for provider management endpoints."""

from pydantic import BaseModel, Field


class ProviderInfoResponse(BaseModel):
    """Current provider status returned to the caller."""

    active_provider: str
    supported_providers: list[str]
    available: bool
    message: str


class SetProviderRequest(BaseModel):
    """Payload for switching the active LLM provider."""

    provider: str = Field(min_length=1, max_length=50)

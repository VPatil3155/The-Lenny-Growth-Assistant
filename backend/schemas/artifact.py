"""Request and response schemas for Markdown artifact generation."""

from typing import Literal

from pydantic import BaseModel, Field


ArtifactType = Literal[
    "marketing_plan",
    "email",
    "growth_strategy",
    "product_launch_plan",
    "meeting_summary",
]


class GenerateArtifactRequest(BaseModel):
    """Payload for one artifact generation request."""

    artifact_type: ArtifactType
    topic: str = Field(min_length=1)
    additional_context: str | None = None


class ArtifactResponse(BaseModel):
    """Generated Markdown artifact returned to the caller."""

    artifact_type: ArtifactType
    title: str
    content: str

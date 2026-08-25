"""HTTP endpoint for generating structured Markdown artifacts."""

from fastapi import APIRouter, HTTPException, status

from schemas.artifact import ArtifactResponse, GenerateArtifactRequest
from services.artifact_service import ArtifactGenerationError, ArtifactService


router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("/generate", response_model=ArtifactResponse)
def generate_artifact(payload: GenerateArtifactRequest) -> ArtifactResponse:
    """Generate a Markdown artifact for the requested type and topic."""

    try:
        artifact = ArtifactService().generate(
            artifact_type=payload.artifact_type,
            topic=payload.topic,
            additional_context=payload.additional_context,
        )
    except ArtifactGenerationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate artifact.",
        )

    return ArtifactResponse(
        artifact_type=artifact.artifact_type,
        title=artifact.title,
        content=artifact.content,
    )

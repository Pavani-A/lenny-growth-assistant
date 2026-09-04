from fastapi import APIRouter, HTTPException

from app.schemas.artifact import ArtifactRequest, ArtifactResponse
from app.services.artifact_service import ArtifactService


router = APIRouter(
    prefix="/api/v1",
    tags=["artifacts"],
)

artifact_service = ArtifactService()


@router.post(
    "/artifacts",
    response_model=ArtifactResponse,
)
def generate_artifact(
    request: ArtifactRequest,
) -> ArtifactResponse:
    """Generate an HTML or Markdown artifact."""

    try:
        artifact = artifact_service.generate(
            prompt=request.prompt,
            session_id=request.session_id,
        )

        return ArtifactResponse(
            session_id=request.session_id,
            provider=request.provider,
            artifact=artifact,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_request",
                "message": str(exc),
            },
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "artifact_generation_failed",
                "message": str(exc),
            },
        ) from exc
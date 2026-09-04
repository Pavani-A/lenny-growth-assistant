from fastapi import APIRouter, HTTPException

from app.schemas.growth_assistant import (
    GrowthAssistantRequest,
    GrowthAssistantResponse,
    GrowthAssistantSource,
)
from app.services.growth_assistant_service import GrowthAssistantService


router = APIRouter(
    prefix="/growth-assistant",
    tags=["Growth Assistant"],
)


@router.post("", response_model=GrowthAssistantResponse)
def growth_assistant(request: GrowthAssistantRequest):
    """Answer a product/growth question using the Pi-based assistant."""

    try:
        service = GrowthAssistantService()

        answer, sources = service.answer(
            message=request.message,
            top_k=request.top_k,
        )

        formatted_sources = [
            GrowthAssistantSource(**source)
            for source in sources
        ]

        return GrowthAssistantResponse(
            answer=answer,
            sources=formatted_sources,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Growth Assistant failed: {exc}",
        ) from exc
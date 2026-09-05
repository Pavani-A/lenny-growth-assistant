import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

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


def _deduplicate_sources(sources: list[dict]) -> list[dict]:
    """Remove duplicate transcript chunks from the source list."""

    unique_sources = []
    seen_sources = set()

    for source in sources:
        source_key = (
            source["episode_title"],
            source["chunk_index"],
        )

        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)
        unique_sources.append(source)

    return unique_sources


@router.post(
    "",
    response_model=GrowthAssistantResponse,
)
def growth_assistant(
    request: GrowthAssistantRequest,
):
    """Answer a product/growth question using the Pi-based assistant."""

    try:
        service = GrowthAssistantService()

        answer, sources = service.answer(
            message=request.message,
            top_k=request.top_k,
        )

        unique_sources = _deduplicate_sources(sources)

        formatted_sources = [
            GrowthAssistantSource(**source)
            for source in unique_sources
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


@router.post("/stream")
def growth_assistant_stream(
    request: GrowthAssistantRequest,
):
    """Stream a grounded answer from the Pi-based assistant."""

    try:
        service = GrowthAssistantService()

        stream, sources = service.stream_answer(
            message=request.message,
            session_id=request.session_id,
            top_k=request.top_k,
        )

        def event_stream():
            try:
                for chunk in stream:
                    yield (
                        "event: token\n"
                        f"data: {json.dumps({'content': chunk})}\n\n"
                    )

                unique_sources = _deduplicate_sources(sources)

                formatted_sources = [
                    GrowthAssistantSource(**source).model_dump(
                        mode="json"
                    )
                    for source in unique_sources
                ]

                yield (
                    "event: sources\n"
                    f"data: {json.dumps({'sources': formatted_sources})}\n\n"
                )

                yield "event: done\ndata: {}\n\n"

            except Exception as exc:
                error_data = json.dumps(
                    {
                        "message": f"Growth Assistant streaming failed: {exc}"
                    }
                )

                yield (
                    "event: error\n"
                    f"data: {error_data}\n\n"
                )

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
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
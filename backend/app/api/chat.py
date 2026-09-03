import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(prefix="/api/v1", tags=["chat"])

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat request using the selected LLM provider."""

    try:
        return chat_service.chat(
            message=request.message,
            session_id=request.session_id,
            provider=request.provider,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_request",
                "message": str(exc),
            },
        ) from exc


@router.post("/chat/stream")
def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Stream an assistant response using Server-Sent Events."""

    try:
        stream, sources = chat_service.chat_stream(
            message=request.message,
            session_id=request.session_id,
            provider=request.provider,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_request",
                "message": str(exc),
            },
        ) from exc

    def event_generator():
        """Convert generated chunks into SSE events."""

        for chunk in stream:
            yield (
                "event: token\n"
                f"data: {json.dumps({'content': chunk})}\n\n"
            )

        yield (
            "event: sources\n"
            f"data: {json.dumps({'sources': sources}, default=str)}\n\n"
        )

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
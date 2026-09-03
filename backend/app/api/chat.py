from fastapi import APIRouter, HTTPException

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
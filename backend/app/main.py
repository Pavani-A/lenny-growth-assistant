from fastapi import FastAPI

from app.api.artifact import router as artifact_router
from app.api.chat import router as chat_router


app = FastAPI(
    title="Lenny Growth Assistant API",
    description="Backend API for the Lenny Growth Assistant",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


app.include_router(chat_router)
app.include_router(artifact_router)
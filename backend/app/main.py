from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.artifact import router as artifact_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router


app = FastAPI(
    title="Lenny Growth Assistant API",
    description="Backend API for the Lenny Growth Assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


app.include_router(chat_router)
app.include_router(artifact_router)
app.include_router(conversations_router)
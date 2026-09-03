from fastapi import FastAPI

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
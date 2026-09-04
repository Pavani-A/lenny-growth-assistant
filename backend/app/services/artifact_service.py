from app.agent.ollama_agent import OllamaGrowthAssistantAgent
from app.schemas.artifact import Artifact


class ArtifactService:
    """Service responsible for generating user-requested artifacts."""

    def __init__(self):
        self.agent = OllamaGrowthAssistantAgent()

    def generate(
        self,
        prompt: str,
        session_id: str,
    ) -> Artifact:
        """Generate an HTML or Markdown artifact."""

        if not prompt.strip():
            raise ValueError("Artifact prompt cannot be empty.")

        if not session_id.strip():
            raise ValueError("Session ID cannot be empty.")

        result = self.agent.run_artifact(
            prompt=prompt,
            session_id=session_id,
        )

        return Artifact(
            type=result["type"],
            title=result["title"],
            content=result["content"],
        )
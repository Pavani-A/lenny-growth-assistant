from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """Structured response returned by the growth assistant agent."""

    answer: str
    sources: list[dict]


class GrowthAssistantAgent(ABC):
    """Common interface for the Lenny Growth Assistant agent."""

    @abstractmethod
    def run(
        self,
        message: str,
        session_id: str,
    ) -> AgentResponse:
        """Process a user message within a conversation session."""
        raise NotImplementedError
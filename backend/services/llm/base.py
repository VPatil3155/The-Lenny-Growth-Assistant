"""Provider-independent interface for language model generation."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Contract implemented by all synchronous LLM providers."""

    @abstractmethod
    def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Generate one assistant response for the supplied conversation."""

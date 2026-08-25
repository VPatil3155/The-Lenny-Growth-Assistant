"""OpenAI implementation of the LLM provider interface."""

from app.config import Settings, get_settings

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """Generate text with the official OpenAI Python SDK."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Return the generated assistant text without streaming."""

        if not self._settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY must be configured to use the OpenAI provider.")

        from openai import OpenAI

        client = OpenAI(api_key=self._settings.openai_api_key)
        response = client.responses.create(
            model=self._settings.openai_model,
            input=messages,
            instructions=system_prompt,
        )
        return response.output_text

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

        from openai import (
            APIConnectionError,
            APIError,
            AuthenticationError,
            OpenAI,
            RateLimitError,
        )

        client = OpenAI(api_key=self._settings.openai_api_key)
        try:
            response = client.responses.create(
                model=self._settings.openai_model,
                input=messages,
                instructions=system_prompt,
            )
        except AuthenticationError as error:
            raise RuntimeError(
                "OpenAI authentication failed. "
                "Verify that OPENAI_API_KEY is a valid API key."
            ) from error
        except RateLimitError as error:
            raise RuntimeError(
                "OpenAI rate limit exceeded. "
                "Wait a moment before retrying or check your usage limits."
            ) from error
        except APIConnectionError as error:
            raise RuntimeError(
                "Could not connect to the OpenAI API. "
                "Check your network connection and try again."
            ) from error
        except APIError as error:
            raise RuntimeError(
                f"OpenAI API returned an error (HTTP {error.status_code}): "
                f"{error.message}"
            ) from error
        return response.output_text

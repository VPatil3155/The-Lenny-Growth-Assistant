"""Ollama implementation of the LLM provider interface."""

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from app.config import Settings, get_settings

from .base import LLMProvider


class OllamaProvider(LLMProvider):
    """Generate text through Ollama's non-streaming REST API."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def generate_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None,
    ) -> str:
        """Return the generated assistant text without streaming."""

        request_messages = list(messages)
        if system_prompt:
            request_messages.insert(0, {"role": "system", "content": system_prompt})

        payload = json.dumps(
            {
                "model": self._settings.ollama_model,
                "messages": request_messages,
                "stream": False,
            }
        ).encode("utf-8")
        request = Request(
            f"{self._settings.ollama_base_url.rstrip('/')}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=120) as response:
                body = json.loads(response.read().decode("utf-8"))
        except URLError as error:
            raise RuntimeError(
                f"Cannot connect to Ollama at {self._settings.ollama_base_url}. "
                "Make sure Ollama is running."
            ) from error
        except TimeoutError as error:
            raise RuntimeError(
                f"Ollama request timed out after 120 seconds at "
                f"{self._settings.ollama_base_url}."
            ) from error
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Ollama returned an invalid JSON response. "
                "The server may be misconfigured or experiencing issues."
            ) from error
        try:
            return body["message"]["content"]
        except (KeyError, TypeError) as error:
            raise RuntimeError(
                "Ollama returned an unexpected response structure. "
                "The response did not contain a 'message.content' field."
            ) from error

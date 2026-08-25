"""Ollama implementation of the LLM provider interface."""

import json
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
        with urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["message"]["content"]

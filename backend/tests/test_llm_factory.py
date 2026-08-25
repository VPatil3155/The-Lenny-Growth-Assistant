"""Tests for configured LLM provider selection."""

from types import SimpleNamespace
import unittest
from unittest.mock import patch

from services.llm.factory import get_llm_provider
from services.llm.ollama_provider import OllamaProvider
from services.llm.openai_provider import OpenAIProvider


def provider_settings(provider: str) -> SimpleNamespace:
    """Build the settings object required by the provider factory."""

    return SimpleNamespace(
        llm_provider=provider,
        openai_api_key=None,
        openai_model="gpt-4.1-mini",
        ollama_base_url="http://localhost:11434",
        ollama_model="llama3.2",
    )


class TestLLMFactory(unittest.TestCase):
    """Verify provider selection remains configuration-driven."""

    def test_get_llm_provider_returns_openai_provider(self) -> None:
        with patch(
            "services.llm.factory.get_settings",
            return_value=provider_settings("openai"),
        ):
            self.assertIsInstance(get_llm_provider(), OpenAIProvider)

    def test_get_llm_provider_returns_ollama_provider(self) -> None:
        with patch(
            "services.llm.factory.get_settings",
            return_value=provider_settings("ollama"),
        ):
            self.assertIsInstance(get_llm_provider(), OllamaProvider)

    def test_get_llm_provider_rejects_unsupported_provider(self) -> None:
        with patch(
            "services.llm.factory.get_settings",
            return_value=provider_settings("unknown"),
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Unsupported LLM_PROVIDER 'unknown'",
            ):
                get_llm_provider()

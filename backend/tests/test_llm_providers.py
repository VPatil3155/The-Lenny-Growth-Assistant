"""Unit tests for LLM provider error handling."""

import json
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock, patch
from urllib.error import URLError


def _install_mock_openai():
    """Install a minimal mock ``openai`` module into ``sys.modules``."""

    mod = ModuleType("openai")

    class _AuthenticationError(Exception):
        pass

    class _RateLimitError(Exception):
        pass

    class _APIConnectionError(Exception):
        pass

    class _APIError(Exception):
        def __init__(self, message="", response=None, body=None):
            self.status_code = getattr(response, "status_code", 500) if response else 500
            self.message = message

    mod.AuthenticationError = _AuthenticationError
    mod.RateLimitError = _RateLimitError
    mod.APIConnectionError = _APIConnectionError
    mod.APIError = _APIError
    mod.OpenAI = MagicMock
    sys.modules["openai"] = mod
    return mod


_mock_openai = _install_mock_openai()


def _ollama_settings():
    return SimpleNamespace(
        ollama_base_url="http://localhost:11434",
        ollama_model="llama3.2",
    )


def _openai_settings(api_key="sk-test-key"):
    return SimpleNamespace(
        openai_api_key=api_key,
        openai_model="gpt-4.1-mini",
    )


class TestOllamaProviderErrorHandling(unittest.TestCase):
    """Verify that OllamaProvider converts low-level errors into RuntimeErrors."""

    def _make_provider(self):
        from services.llm.ollama_provider import OllamaProvider

        return OllamaProvider(settings=_ollama_settings())

    def test_connection_error_returns_descriptive_message(self):
        provider = self._make_provider()
        with patch(
            "services.llm.ollama_provider.urlopen",
            side_effect=URLError(ConnectionRefusedError),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("Cannot connect to Ollama", str(ctx.exception))

    def test_timeout_error_returns_descriptive_message(self):
        provider = self._make_provider()
        with patch(
            "services.llm.ollama_provider.urlopen",
            side_effect=TimeoutError("timed out"),
        ):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("timed out", str(ctx.exception))

    def test_json_decode_error_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_response = Mock()
        mock_response.read.return_value = b"not-json"
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch("services.llm.ollama_provider.urlopen", return_value=mock_response):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("invalid JSON", str(ctx.exception))

    def test_missing_message_key_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"error": "fail"}).encode()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch("services.llm.ollama_provider.urlopen", return_value=mock_response):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("unexpected response structure", str(ctx.exception))

    def test_successful_response_returns_content(self):
        provider = self._make_provider()
        mock_response = Mock()
        body = {"message": {"content": "Hello from Ollama"}}
        mock_response.read.return_value = json.dumps(body).encode()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        with patch("services.llm.ollama_provider.urlopen", return_value=mock_response):
            result = provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertEqual(result, "Hello from Ollama")


class TestOpenAIProviderErrorHandling(unittest.TestCase):
    """Verify that OpenAIProvider converts SDK errors into RuntimeErrors."""

    def _make_provider(self, api_key="sk-test-key"):
        from services.llm.openai_provider import OpenAIProvider

        return OpenAIProvider(settings=_openai_settings(api_key=api_key))

    def test_missing_api_key_raises_runtime_error(self):
        provider = self._make_provider(api_key=None)
        with self.assertRaises(RuntimeError) as ctx:
            provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("OPENAI_API_KEY", str(ctx.exception))

    def test_authentication_error_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_client = MagicMock()
        mock_client.responses.create.side_effect = _mock_openai.AuthenticationError(
            "Invalid API key",
        )

        with patch("openai.OpenAI", return_value=mock_client):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("authentication failed", str(ctx.exception).lower())

    def test_rate_limit_error_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_client = MagicMock()
        mock_client.responses.create.side_effect = _mock_openai.RateLimitError(
            "Rate limit exceeded",
        )

        with patch("openai.OpenAI", return_value=mock_client):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("rate limit", str(ctx.exception).lower())

    def test_api_connection_error_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_client = MagicMock()
        mock_client.responses.create.side_effect = _mock_openai.APIConnectionError(
            "Connection failed",
        )

        with patch("openai.OpenAI", return_value=mock_client):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertIn("Could not connect", str(ctx.exception))

    def test_api_error_returns_descriptive_message(self):
        provider = self._make_provider()
        mock_client = MagicMock()
        exc = _mock_openai.APIError("Internal server error")
        mock_client.responses.create.side_effect = exc

        with patch("openai.OpenAI", return_value=mock_client):
            with self.assertRaises(RuntimeError) as ctx:
                provider.generate_response([{"role": "user", "content": "Hi"}])

        msg = str(ctx.exception)
        self.assertIn("500", msg)
        self.assertIn("Internal server error", msg)

    def test_successful_response_returns_output_text(self):
        provider = self._make_provider()
        mock_client = MagicMock()
        mock_response = Mock()
        mock_response.output_text = "Hello from OpenAI"
        mock_client.responses.create.return_value = mock_response

        with patch("openai.OpenAI", return_value=mock_client):
            result = provider.generate_response([{"role": "user", "content": "Hi"}])

        self.assertEqual(result, "Hello from OpenAI")

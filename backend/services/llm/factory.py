"""Factory for selecting the configured LLM provider."""

from app.config import get_settings

from .base import LLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider


def get_llm_provider() -> LLMProvider:
    """Return an LLM provider based on the LLM_PROVIDER setting."""

    settings = get_settings()
    provider_name = settings.llm_provider.lower()

    if provider_name == "openai":
        return OpenAIProvider(settings)
    if provider_name == "ollama":
        return OllamaProvider(settings)

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER '{settings.llm_provider}'. "
        "Supported providers are: openai, ollama."
    )

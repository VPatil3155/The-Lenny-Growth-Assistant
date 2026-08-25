"""Factory for selecting the configured LLM provider."""

from urllib.error import URLError
from urllib.request import Request, urlopen

from app.config import get_settings

from .base import LLMProvider
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider

SUPPORTED_PROVIDERS = ("ollama", "openai")

_provider_override: str | None = None


def get_active_provider_name() -> str:
    """Return the currently active provider name."""
    if _provider_override is not None:
        return _provider_override
    return get_settings().llm_provider.lower()


def set_provider_override(provider_name: str | None) -> None:
    """Override the provider at runtime. Pass None to revert to .env."""
    global _provider_override
    if provider_name is not None:
        provider_name = provider_name.lower()
        if provider_name not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider '{provider_name}'. "
                f"Supported: {', '.join(SUPPORTED_PROVIDERS)}."
            )
    _provider_override = provider_name


def get_llm_provider() -> LLMProvider:
    """Return an LLM provider based on the active provider setting."""

    settings = get_settings()
    provider_name = get_active_provider_name()

    if provider_name == "openai":
        return OpenAIProvider(settings)
    if provider_name == "ollama":
        return OllamaProvider(settings)

    raise RuntimeError(
        f"Unsupported LLM_PROVIDER '{provider_name}'. "
        f"Supported providers are: {', '.join(SUPPORTED_PROVIDERS)}."
    )


def check_provider_availability(provider_name: str) -> dict[str, str | bool]:
    """Check whether a provider is reachable / configured.

    Returns a dict with keys: available (bool), message (str).
    """
    provider_name = provider_name.lower()
    settings = get_settings()

    if provider_name == "ollama":
        try:
            url = f"{settings.ollama_base_url.rstrip('/')}/api/tags"
            req = Request(url, method="GET")
            with urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return {"available": True, "message": "Ollama is running."}
        except (URLError, OSError, TimeoutError):
            pass
        return {
            "available": False,
            "message": (
                f"Cannot reach Ollama at {settings.ollama_base_url}. "
                "Make sure Ollama is running."
            ),
        }

    if provider_name == "openai":
        if settings.openai_api_key:
            return {"available": True, "message": "OpenAI API key is configured."}
        return {
            "available": False,
            "message": "OPENAI_API_KEY is not set. Add it to your .env file.",
        }

    return {
        "available": False,
        "message": f"Unknown provider '{provider_name}'.",
    }

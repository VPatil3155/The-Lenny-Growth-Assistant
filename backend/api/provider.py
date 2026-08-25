"""HTTP endpoints for LLM provider management."""

from fastapi import APIRouter, HTTPException, status

from schemas.provider import ProviderInfoResponse, SetProviderRequest
from services.llm import (
    SUPPORTED_PROVIDERS,
    check_provider_availability,
    get_active_provider_name,
    set_provider_override,
)


router = APIRouter(prefix="/provider", tags=["provider"])


@router.get("", response_model=ProviderInfoResponse)
def get_provider_info() -> ProviderInfoResponse:
    """Return the current active provider and its availability."""
    active = get_active_provider_name()
    availability = check_provider_availability(active)
    return ProviderInfoResponse(
        active_provider=active,
        supported_providers=list(SUPPORTED_PROVIDERS),
        available=availability["available"],
        message=availability["message"],
    )


@router.post("", response_model=ProviderInfoResponse)
def set_provider(payload: SetProviderRequest) -> ProviderInfoResponse:
    """Switch the active LLM provider at runtime."""
    provider_name = payload.provider.strip().lower()

    if provider_name not in SUPPORTED_PROVIDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported provider '{provider_name}'. "
                f"Supported: {', '.join(SUPPORTED_PROVIDERS)}."
            ),
        )

    set_provider_override(provider_name)
    availability = check_provider_availability(provider_name)
    return ProviderInfoResponse(
        active_provider=provider_name,
        supported_providers=list(SUPPORTED_PROVIDERS),
        available=availability["available"],
        message=availability["message"],
    )

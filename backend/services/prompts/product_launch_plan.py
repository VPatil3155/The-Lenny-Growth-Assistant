"""Prompt template for product launch plans."""

from ._base import build_messages


INSTRUCTIONS = """Create a product launch plan with goals, audience, launch phases,
go-to-market activities, risks, ownership, and measurable success criteria."""


def build_prompt(topic: str, additional_context: str | None) -> list[dict[str, str]]:
    """Build messages for a product launch plan."""

    return build_messages(INSTRUCTIONS, topic, additional_context)

"""Prompt template for meeting summaries."""

from ._base import build_messages


INSTRUCTIONS = """Create a clear meeting summary with key discussion points,
decisions, action items, owners when supplied, and next steps."""


def build_prompt(topic: str, additional_context: str | None) -> list[dict[str, str]]:
    """Build messages for a meeting summary."""

    return build_messages(INSTRUCTIONS, topic, additional_context)

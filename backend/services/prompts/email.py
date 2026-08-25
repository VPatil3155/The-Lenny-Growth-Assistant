"""Prompt template for emails."""

from ._base import build_messages


INSTRUCTIONS = """Write a concise, audience-appropriate email with a clear subject line,
helpful body copy, and a specific call to action."""


def build_prompt(topic: str, additional_context: str | None) -> list[dict[str, str]]:
    """Build messages for an email."""

    return build_messages(INSTRUCTIONS, topic, additional_context)

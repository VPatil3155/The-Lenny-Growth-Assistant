"""Prompt template for marketing plans."""

from ._base import build_messages


INSTRUCTIONS = """Create a practical marketing plan with target audience, positioning,
channels, campaign ideas, timeline, budget considerations, and success metrics."""


def build_prompt(topic: str, additional_context: str | None) -> list[dict[str, str]]:
    """Build messages for a marketing plan."""

    return build_messages(INSTRUCTIONS, topic, additional_context)

"""Prompt template for growth strategies."""

from ._base import build_messages


INSTRUCTIONS = """Create an actionable growth strategy covering objectives, target
segments, acquisition and retention experiments, prioritization, and metrics."""


def build_prompt(topic: str, additional_context: str | None) -> list[dict[str, str]]:
    """Build messages for a growth strategy."""

    return build_messages(INSTRUCTIONS, topic, additional_context)

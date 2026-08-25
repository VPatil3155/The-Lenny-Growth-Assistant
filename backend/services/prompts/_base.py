"""Shared helpers for artifact-generation prompt templates."""


def build_messages(
    instructions: str, topic: str, additional_context: str | None
) -> list[dict[str, str]]:
    """Build the provider message list for one structured artifact request."""

    context = additional_context.strip() if additional_context else "None provided."
    return [
        {"role": "system", "content": instructions},
        {
            "role": "user",
            "content": (
                f"Topic:\n{topic}\n\nAdditional Context:\n{context}\n\n"
                "Return Markdown only. Begin with a level-one Markdown heading that "
                "serves as the artifact title."
            ),
        },
    ]

"""Generate Markdown artifacts through the configured LLM provider."""

import re
from dataclasses import dataclass
from typing import Callable

from services.llm.factory import get_llm_provider
from services.prompts import (
    email,
    growth_strategy,
    marketing_plan,
    meeting_summary,
    product_launch_plan,
)


PromptTemplate = Callable[[str, str | None], list[dict[str, str]]]
PROMPT_TEMPLATES: dict[str, PromptTemplate] = {
    "marketing_plan": marketing_plan.build_prompt,
    "email": email.build_prompt,
    "growth_strategy": growth_strategy.build_prompt,
    "product_launch_plan": product_launch_plan.build_prompt,
    "meeting_summary": meeting_summary.build_prompt,
}
TITLE_PATTERN = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Artifact:
    """Generated Markdown artifact returned to the API layer."""

    artifact_type: str
    title: str
    content: str


class ArtifactGenerationError(Exception):
    """Raised when an LLM provider cannot generate an artifact."""


class ArtifactService:
    """Generate supported artifacts using the existing configured LLM provider."""

    def generate(
        self, artifact_type: str, topic: str, additional_context: str | None = None
    ) -> Artifact:
        """Generate one Markdown artifact from its type-specific prompt template."""

        template = PROMPT_TEMPLATES.get(artifact_type)
        if template is None:
            raise ValueError(f"Unsupported artifact type: {artifact_type}")

        try:
            content = get_llm_provider().generate_response(
                template(topic, additional_context)
            ).strip()
        except Exception as error:
            raise ArtifactGenerationError("Unable to generate artifact.") from error

        return Artifact(
            artifact_type=artifact_type,
            title=self._extract_title(content, topic),
            content=content,
        )

    @staticmethod
    def _extract_title(content: str, fallback: str) -> str:
        """Use the first Markdown heading as title, with a sensible fallback."""

        match = TITLE_PATTERN.search(content)
        return match.group(1).strip() if match else fallback.strip()

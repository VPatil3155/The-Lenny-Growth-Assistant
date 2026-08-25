"""Unit tests for Markdown artifact generation."""

import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from api.artifacts import generate_artifact
from schemas.artifact import GenerateArtifactRequest
from services.artifact_service import (
    Artifact,
    ArtifactGenerationError,
    ArtifactService,
    PROMPT_TEMPLATES,
)


class TestArtifactService(unittest.TestCase):
    """Verify artifact generation without calling an LLM service."""

    def test_generates_markdown_artifact_with_title(self):
        provider = Mock()
        provider.generate_response.return_value = "# Resume Builder Launch Plan\n\n- Launch on campus"

        with patch("services.artifact_service.get_llm_provider", return_value=provider):
            artifact = ArtifactService().generate(
                "marketing_plan",
                "Launch an AI resume builder",
                "Target audience is university students.",
            )

        self.assertEqual(artifact.artifact_type, "marketing_plan")
        self.assertEqual(artifact.title, "Resume Builder Launch Plan")
        self.assertTrue(artifact.content.startswith("# Resume Builder Launch Plan"))
        messages = provider.generate_response.call_args.args[0]
        self.assertIn("marketing plan", messages[0]["content"].lower())
        self.assertIn("Launch an AI resume builder", messages[1]["content"])

    def test_all_artifact_types_have_a_prompt_template(self):
        self.assertEqual(
            set(PROMPT_TEMPLATES),
            {
                "marketing_plan",
                "email",
                "growth_strategy",
                "product_launch_plan",
                "meeting_summary",
            },
        )

    def test_provider_failure_is_wrapped(self):
        provider = Mock()
        provider.generate_response.side_effect = RuntimeError("unavailable")

        with patch("services.artifact_service.get_llm_provider", return_value=provider):
            with self.assertRaises(ArtifactGenerationError):
                ArtifactService().generate("email", "Welcome email")

    def test_endpoint_returns_generated_markdown(self):
        generated = Artifact(
            artifact_type="email", title="Welcome", content="# Welcome\n\nHello!"
        )
        with patch.object(ArtifactService, "generate", return_value=generated):
            response = generate_artifact(
                GenerateArtifactRequest(artifact_type="email", topic="Welcome email")
            )

        self.assertEqual(response.model_dump(), generated.__dict__)

    def test_endpoint_maps_generation_failures_to_500(self):
        with patch.object(
            ArtifactService, "generate", side_effect=ArtifactGenerationError
        ):
            with self.assertRaises(HTTPException) as error:
                generate_artifact(
                    GenerateArtifactRequest(artifact_type="email", topic="Welcome email")
                )

        self.assertEqual(error.exception.status_code, 500)

    def test_openapi_documents_artifact_generation(self):
        from app.main import app

        operation = app.openapi()["paths"]["/artifacts/generate"]["post"]
        self.assertIn("ArtifactResponse", str(operation["responses"]["200"]))

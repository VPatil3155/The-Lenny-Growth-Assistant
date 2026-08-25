"""Unit tests for the chat orchestration flow."""

from datetime import datetime, timezone
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from uuid import uuid4

from fastapi import HTTPException

from api.messages import create_chat_message
from schemas.chat_message import CreateMessageRequest
from services.chat_orchestrator import (
    ChatOrchestrator,
    LLMProviderError,
    SessionNotFoundError,
)


def message(session_id, role, content):
    """Create a lightweight object resembling a persisted chat message."""

    return SimpleNamespace(
        id=uuid4(),
        session_id=session_id,
        role=role,
        content=content,
        created_at=datetime.now(timezone.utc),
    )


class TestChatOrchestrator(unittest.TestCase):
    """Verify provider integration without contacting an LLM."""

    def test_loads_history_generates_and_persists_assistant(self):
        session_id = uuid4()
        db = Mock()
        previous_user = message(session_id, "user", "How do I get started?")
        previous_assistant = message(
            session_id, "assistant", "Start with one user segment."
        )
        user_message = message(session_id, "user", "What should I measure?")
        assistant_message = message(
            session_id, "assistant", "Measure activation weekly."
        )
        provider = Mock()
        provider.generate_response.return_value = assistant_message.content

        with (
            patch("services.chat_orchestrator.get_session", return_value=object()),
            patch(
                "services.chat_orchestrator.create_message",
                side_effect=[user_message, assistant_message],
            ) as create_message,
            patch(
                "services.chat_orchestrator.get_messages",
                return_value=[previous_user, previous_assistant, user_message],
            ) as get_messages,
            patch("services.chat_orchestrator.get_llm_provider", return_value=provider),
        ):
            result = ChatOrchestrator(db).create_response(session_id, user_message.content)

        self.assertEqual(result, (user_message, assistant_message))
        get_messages.assert_called_once_with(db, session_id)
        provider.generate_response.assert_called_once_with(
            [
                {
                    "role": "system",
                    "content": (
                        "System Prompt:\nYou are Lenny, a startup growth assistant.\n\n"
                        "Relevant Context:\nNo relevant context found."
                    ),
                },
                {"role": "user", "content": previous_user.content},
                {"role": "assistant", "content": previous_assistant.content},
                {"role": "user", "content": user_message.content},
            ]
        )
        self.assertEqual(
            create_message.call_args_list[1].args,
            (db, session_id, "assistant", assistant_message.content),
        )

    def test_provider_failure_does_not_persist_assistant(self):
        session_id = uuid4()
        provider = Mock()
        provider.generate_response.side_effect = RuntimeError("provider unavailable")

        with (
            patch("services.chat_orchestrator.get_session", return_value=object()),
            patch(
                "services.chat_orchestrator.create_message",
                return_value=message(session_id, "user", "Hi"),
            ) as create_message,
            patch("services.chat_orchestrator.get_messages", return_value=[]),
            patch("services.chat_orchestrator.get_llm_provider", return_value=provider),
        ):
            with self.assertRaises(LLMProviderError):
                ChatOrchestrator(Mock()).create_response(session_id, "Hi")

        self.assertEqual(create_message.call_count, 1)

    def test_endpoint_returns_both_persisted_messages(self):
        session_id = uuid4()
        user_message = message(session_id, "user", "Hello")
        assistant_message = message(session_id, "assistant", "Hi, how can I help?")

        with patch.object(
            ChatOrchestrator,
            "create_response",
            return_value=(user_message, assistant_message),
        ):
            response = create_chat_message(
                session_id, CreateMessageRequest(content="Hello"), Mock()
            )

        self.assertEqual(response.user_message.id, user_message.id)
        self.assertEqual(response.assistant_message.id, assistant_message.id)
        self.assertEqual(response.assistant_message.content, assistant_message.content)

    def test_endpoint_maps_missing_session_to_404(self):
        with patch.object(
            ChatOrchestrator, "create_response", side_effect=SessionNotFoundError
        ):
            with self.assertRaises(HTTPException) as error:
                create_chat_message(uuid4(), CreateMessageRequest(content="Hi"), Mock())

        self.assertEqual(error.exception.status_code, 404)

    def test_endpoint_maps_provider_failure_to_500(self):
        with patch.object(
            ChatOrchestrator, "create_response", side_effect=LLMProviderError
        ):
            with self.assertRaises(HTTPException) as error:
                create_chat_message(uuid4(), CreateMessageRequest(content="Hi"), Mock())

        self.assertEqual(error.exception.status_code, 500)

    def test_openapi_documents_the_chat_turn_response(self):
        from app.main import app

        operation = app.openapi()["paths"]["/sessions/{session_id}/messages"]["post"]
        self.assertIn("ChatTurnResponse", str(operation["responses"]["201"]))

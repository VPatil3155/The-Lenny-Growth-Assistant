"""Coordinate persisted chat history with the configured LLM provider."""

from uuid import UUID

from sqlalchemy.orm import Session

from models.chat_message import ChatMessage
from rag.index import get_rag_index
from rag.prompt_builder import PromptBuilder
from services.chat_message_service import create_message, get_messages
from services.chat_session_service import DEFAULT_SESSION_TITLE, get_session
from services.llm.factory import get_llm_provider
from services.title_generator import generate_title


SYSTEM_PROMPT = "You are Lenny, a startup growth assistant."


class SessionNotFoundError(Exception):
    """Raised when attempting to chat in a session that does not exist."""


class LLMProviderError(Exception):
    """Raised when the configured LLM provider cannot generate a response."""


class ChatOrchestrator:
    """Persist a user turn, generate an answer, and persist the answer."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_response(
        self, session_id: UUID, content: str
    ) -> tuple[ChatMessage, ChatMessage, "ChatSession | None"]:
        """Create a complete user/assistant chat turn for ``session_id``.

        The user message, assistant message, and any auto-generated title
        update are committed in a **single database transaction**.  If the
        LLM call fails the entire transaction is rolled back so no
        partial state is persisted.

        Returns the user message, assistant message, and optionally the
        updated session (set when auto-titling occurs).
        """

        chat_session = get_session(self._db, session_id)
        if chat_session is None:
            raise SessionNotFoundError("Session not found.")

        user_message = create_message(self._db, session_id, "user", content, commit=False)
        persisted_messages = get_messages(self._db, session_id)
        conversation_history = [
            {"role": message.role, "content": message.content}
            for message in persisted_messages
            if message.id != user_message.id
        ]
        relevant_chunks = get_rag_index().retrieve(content)
        history = PromptBuilder.build_messages(
            system_prompt=SYSTEM_PROMPT,
            relevant_chunks=relevant_chunks,
            conversation_history=conversation_history,
            current_user_message=content,
        )

        try:
            assistant_content = get_llm_provider().generate_response(history)
        except Exception as error:
            self._db.rollback()
            raise LLMProviderError("Unable to generate an assistant response.") from error

        assistant_message = create_message(
            self._db, session_id, "assistant", assistant_content, commit=False
        )

        updated_session = None
        if chat_session.title == DEFAULT_SESSION_TITLE:
            chat_session.title = generate_title(content)
            updated_session = chat_session

        self._db.commit()
        if updated_session is not None:
            self._db.refresh(updated_session)

        return user_message, assistant_message, updated_session

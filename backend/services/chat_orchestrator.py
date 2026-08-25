"""Coordinate persisted chat history with the configured LLM provider."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.config import get_settings
from models.chat_message import ChatMessage
from rag.chunker import chunk_documents
from rag.document_loader import DocumentLoader
from rag.prompt_builder import PromptBuilder
from rag.retriever import KeywordRetriever
from services.chat_message_service import create_message, get_messages
from services.chat_session_service import get_session
from services.llm.factory import get_llm_provider


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
    ) -> tuple[ChatMessage, ChatMessage]:
        """Create a complete user/assistant chat turn for ``session_id``."""

        if get_session(self._db, session_id) is None:
            raise SessionNotFoundError("Session not found.")

        user_message = create_message(self._db, session_id, "user", content)
        persisted_messages = get_messages(self._db, session_id)
        conversation_history = [
            {"role": message.role, "content": message.content}
            for message in persisted_messages
            if message.id != user_message.id
        ]
        documents = DocumentLoader(get_settings().knowledge_base_path).load()
        relevant_chunks = KeywordRetriever(chunk_documents(documents)).retrieve(content)
        history = PromptBuilder.build_messages(
            system_prompt=SYSTEM_PROMPT,
            relevant_chunks=relevant_chunks,
            conversation_history=conversation_history,
            current_user_message=content,
        )

        try:
            assistant_content = get_llm_provider().generate_response(history)
        except Exception as error:
            raise LLMProviderError("Unable to generate an assistant response.") from error

        assistant_message = create_message(
            self._db, session_id, "assistant", assistant_content
        )
        return user_message, assistant_message

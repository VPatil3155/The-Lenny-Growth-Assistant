"""Thread-safe lazy-initialized RAG index backed by the local knowledge base."""

import threading
from pathlib import Path

from app.config import get_settings
from rag.chunker import DocumentChunk, chunk_documents
from rag.document_loader import DocumentLoader
from rag.retriever import KeywordRetriever


class RAGIndex:
    """Pre-loaded document chunks and retriever for keyword-based retrieval."""

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self._retriever = KeywordRetriever(chunks)

    def retrieve(self, query: str, limit: int = 3) -> list[DocumentChunk]:
        """Return up to ``limit`` chunks matching the query keywords."""

        return self._retriever.retrieve(query, limit)


_index: RAGIndex | None = None
_lock = threading.Lock()


def get_rag_index() -> RAGIndex:
    """Return the singleton RAG index, building it on first access."""

    global _index
    if _index is None:
        with _lock:
            if _index is None:
                _index = _build_index()
    return _index


def _build_index() -> RAGIndex:
    """Load documents, chunk them, and return a ready-to-use index."""

    settings = get_settings()
    documents = DocumentLoader(settings.knowledge_base_path).load()
    chunks = chunk_documents(documents)
    return RAGIndex(chunks)

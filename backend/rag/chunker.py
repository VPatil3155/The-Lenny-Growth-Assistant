"""Split knowledge-base documents into retrieval-sized text chunks."""

from dataclasses import dataclass
from hashlib import sha256

from .document_loader import Document


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


@dataclass(frozen=True)
class DocumentChunk:
    """A source-attributed segment of a loaded document."""

    id: str
    text: str
    source: str


def chunk_documents(
    documents: list[Document],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[DocumentChunk]:
    """Split documents into fixed-width character chunks with overlap."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size.")

    chunks = []
    step = chunk_size - overlap
    for document in documents:
        for start in range(0, len(document.text), step):
            text = document.text[start : start + chunk_size]
            if not text:
                continue
            chunk_id = sha256(
                f"{document.source}:{start}:{text}".encode("utf-8")
            ).hexdigest()
            chunks.append(DocumentChunk(id=chunk_id, text=text, source=document.source))
            if start + chunk_size >= len(document.text):
                break
    return chunks

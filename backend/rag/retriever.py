"""Simple, deterministic keyword retrieval for document chunks."""

import re

from .chunker import DocumentChunk


WORD_PATTERN = re.compile(r"\b\w+\b", re.UNICODE)


def keywords(text: str) -> set[str]:
    """Normalize text to unique case-insensitive word tokens."""

    return {word.lower() for word in WORD_PATTERN.findall(text)}


class KeywordRetriever:
    """Rank chunks by the number of query keywords they contain."""

    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self._chunks = chunks

    def retrieve(self, query: str, limit: int = 3) -> list[DocumentChunk]:
        """Return up to ``limit`` chunks with at least one matching keyword."""

        if limit <= 0:
            return []

        query_keywords = keywords(query)
        if not query_keywords:
            return []

        scored_chunks = [
            (len(query_keywords & keywords(chunk.text)), index, chunk)
            for index, chunk in enumerate(self._chunks)
        ]
        return [
            chunk
            for score, _, chunk in sorted(scored_chunks, key=lambda item: (-item[0], item[1]))
            if score > 0
        ][:limit]

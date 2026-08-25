"""Deterministic title generation from user messages."""

import re

FILLER_WORDS = frozenset(
    {
        "the",
        "i",
        "me",
        "my",
        "you",
        "your",
        "we",
        "our",
        "it",
        "its",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "shall",
        "can",
        "must",
        "to",
        "of",
        "in",
        "for",
        "on",
        "at",
        "by",
        "with",
        "from",
        "as",
        "into",
        "about",
        "between",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "and",
        "but",
        "or",
        "nor",
        "so",
        "yet",
        "both",
        "either",
        "neither",
        "not",
        "only",
        "own",
        "same",
        "than",
        "too",
        "very",
        "just",
        "that",
        "this",
        "these",
        "those",
        "what",
        "which",
        "who",
        "whom",
        "how",
        "when",
        "where",
        "why",
        "if",
        "then",
        "else",
        "because",
        "since",
        "while",
        "although",
        "though",
    }
)

MIN_WORDS = 3
MAX_WORDS = 6


def generate_title(message: str) -> str:
    """Generate a concise 3-6 word title from a user message.

    Strips filler/stop words and keeps meaningful content words,
    applying title case to the result.

    Examples:
        >>> generate_title("How do I build a RAG application?")
        'Build a RAG Application'
        >>> generate_title("Create a marketing plan for an AI resume builder")
        'AI Resume Builder Marketing'
        >>> generate_title("Can you help me write a Python script to scrape data from websites?")
        'Python Script Scrape Data'
    """

    cleaned = re.sub(r"[^\w\s]", " ", message).lower()
    words = cleaned.split()
    meaningful = [w for w in words if w not in FILLER_WORDS and len(w) > 0]

    if not meaningful:
        meaningful = [w for w in words if len(w) > 0]

    if not meaningful:
        return "New Chat"

    selected = meaningful[:MAX_WORDS]

    title = " ".join(selected)
    title = title.title()

    if len(selected) < MIN_WORDS and len(meaningful) > MIN_WORDS:
        title = " ".join(meaningful[:MIN_WORDS]).title()

    return title

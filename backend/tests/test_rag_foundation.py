"""Unit tests for the local keyword-retrieval foundation."""

import unittest

from rag.chunker import DocumentChunk, chunk_documents
from rag.document_loader import Document
from rag.prompt_builder import PromptBuilder
from rag.retriever import KeywordRetriever


class TestRagFoundation(unittest.TestCase):
    """Exercise chunking, retrieval, and provider-ready prompt construction."""

    def test_chunker_creates_overlapping_chunks(self):
        document = Document(text="abcdefghij", source="notes.md", metadata={})

        chunks = chunk_documents([document], chunk_size=5, overlap=2)

        self.assertEqual([chunk.text for chunk in chunks], ["abcde", "defgh", "ghij"])
        self.assertTrue(all(chunk.source == "notes.md" for chunk in chunks))
        self.assertEqual(len({chunk.id for chunk in chunks}), 3)

    def test_retriever_returns_top_keyword_matches(self):
        chunks = [
            DocumentChunk("one", "Retention improves with onboarding", "retention.md"),
            DocumentChunk("two", "Activation and retention define growth", "growth.md"),
            DocumentChunk("three", "Brand design principles", "brand.md"),
        ]

        results = KeywordRetriever(chunks).retrieve("activation retention", limit=3)

        self.assertEqual([chunk.id for chunk in results], ["two", "one"])

    def test_prompt_builder_orders_context_history_and_current_message(self):
        messages = PromptBuilder.build_messages(
            system_prompt="You are Lenny.",
            relevant_chunks=[DocumentChunk("one", "Track activation.", "guide.md")],
            conversation_history=[{"role": "assistant", "content": "Welcome."}],
            current_user_message="How should I measure growth?",
        )

        self.assertEqual(messages[0]["role"], "system")
        self.assertIn("System Prompt:\nYou are Lenny.", messages[0]["content"])
        self.assertIn("Relevant Context:\nSource: guide.md\nTrack activation.", messages[0]["content"])
        self.assertEqual(messages[1], {"role": "assistant", "content": "Welcome."})
        self.assertEqual(
            messages[2],
            {"role": "user", "content": "How should I measure growth?"},
        )

"""Build provider-ready chat prompts enriched with retrieved context."""

from .chunker import DocumentChunk


class PromptBuilder:
    """Compose system context, conversation history, and the current user turn."""

    @staticmethod
    def build_messages(
        system_prompt: str,
        relevant_chunks: list[DocumentChunk],
        conversation_history: list[dict[str, str]],
        current_user_message: str,
    ) -> list[dict[str, str]]:
        """Return messages in system, history, current-user order for an LLM."""

        context = (
            "\n\n".join(
                f"Source: {chunk.source}\n{chunk.text}" for chunk in relevant_chunks
            )
            or "No relevant context found."
        )
        system_content = (
            f"System Prompt:\n{system_prompt}\n\n"
            f"Relevant Context:\n{context}"
        )
        return [
            {"role": "system", "content": system_content},
            *conversation_history,
            {"role": "user", "content": current_user_message},
        ]

# Session 02 – Retrieval-Augmented Generation (RAG)

## Objective

Add contextual document retrieval to improve chat responses.

---

## Prompt

Implement a lightweight RAG pipeline that:

- Loads Markdown documents
- Splits them into chunks
- Retrieves relevant context
- Injects the context into every LLM request

---

## Result

Implemented:

- Document loader
- Chunking
- Keyword retrieval
- Prompt context injection

---

## Issue Encountered

Relevant documents were being loaded repeatedly for every request.

---

## Resolution

Introduced a cached RAG index to avoid repeated loading and improve performance.

---

## Outcome

✓ Knowledge documents are loaded

✓ Context is retrieved

✓ Responses include retrieved information

✓ Performance improved
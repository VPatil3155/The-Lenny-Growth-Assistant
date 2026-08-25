"""Load supported knowledge-base documents from the local filesystem."""

from dataclasses import dataclass
from pathlib import Path


SUPPORTED_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True)
class Document:
    """Document content and metadata made available to retrieval."""

    text: str
    source: str
    metadata: dict[str, str]


class DocumentLoader:
    """Read UTF-8 Markdown and text files from one knowledge directory."""

    def __init__(self, knowledge_base_path: Path | str) -> None:
        self._knowledge_base_path = Path(knowledge_base_path)

    def load(self) -> list[Document]:
        """Return all supported documents, ordered deterministically by path."""

        if not self._knowledge_base_path.is_dir():
            return []

        documents = []
        for path in sorted(self._knowledge_base_path.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue

            source = str(path.relative_to(self._knowledge_base_path))
            documents.append(
                Document(
                    text=path.read_text(encoding="utf-8"),
                    source=source,
                    metadata={
                        "source": source,
                        "path": str(path),
                        "file_type": path.suffix.lower(),
                    },
                )
            )
        return documents

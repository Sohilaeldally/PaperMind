from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class DocumentChunk:
    id: UUID
    document_id: UUID
    chunk_index: int
    chunk_text: str
    created_at: datetime | None = None
    embedding: list[float] | None = None


from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    CHUNKING = "chunking"
    CHUNKED = "chunked"
    EMBEDDING = "embedding"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass(slots=True)
class Document:
    id: UUID
    original_name: str
    stored_name: str
    content_type: str
    file_size: int
    status: DocumentStatus
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


    
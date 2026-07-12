from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Document:
    id: UUID
    original_name: str
    stored_name: str
    content_type: str
    file_size: int
    status: str
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
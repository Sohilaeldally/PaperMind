from uuid import UUID
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    document_id: UUID | None = None
    top_k: int = 5


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    section_name: str | None
    text: str
    distance: float


class SourceInfo(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    section_name: str | None
    distance: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceInfo]
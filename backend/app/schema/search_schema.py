from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    distance: float

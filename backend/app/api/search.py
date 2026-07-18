from fastapi import APIRouter
from app.schema.search_schema import SearchRequest, SearchResult
from app.services.search_service import search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=list[SearchResult])
async def search_documents(request: SearchRequest):
    return search(request.query, top_k=request.top_k)
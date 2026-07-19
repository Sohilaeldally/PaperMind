from fastapi import APIRouter
from app.schema.search_schema import SearchRequest, SearchResult, AskResponse, SearchInfo
from app.services.search_service import search,ask

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=list[SearchResult])
async def search_documents(request: SearchRequest):
    return search(request.query, top_k=request.top_k)


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: SearchRequest):
    return ask(request.query, top_k=request.top_k)
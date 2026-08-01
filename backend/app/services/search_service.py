from uuid import UUID
from app.services.embedding_service import generate_query_embedding
from app.services.generation_service import generate_answer
from app.db.document_chunk_repository import search_similar_chunks


def _retrieve(query: str, document_id: UUID | None = None, top_k: int = 5):
    query_embedding = generate_query_embedding(query)
    return search_similar_chunks(query_embedding, document_id=document_id, top_k=top_k)


def search(query: str, document_id: UUID | None = None, top_k: int = 5):
    results = _retrieve(query, document_id, top_k)
    return [
        {
            "chunk_id": str(chunk.id),
            "document_id": str(chunk.document_id),
            "chunk_index": chunk.chunk_index,
            "section_name": chunk.section_name,
            "text": chunk.chunk_text,
            "distance": distance,
        }
        for chunk, distance in results
    ]


def ask(query: str, document_id: UUID | None = None, top_k: int = 5) -> dict:
    results = _retrieve(query, document_id, top_k)
    context_chunks = [chunk.chunk_text for chunk, _ in results]
    answer = generate_answer(query, context_chunks)

    sources = [
        {
            "chunk_id": str(chunk.id),
            "document_id": str(chunk.document_id),
            "chunk_index": chunk.chunk_index,
            "section_name": chunk.section_name,
            "distance": distance,
        }
        for chunk, distance in results
    ]

    return {"answer": answer, "sources": sources}
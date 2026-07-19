from app.services.embedding_service import generate_query_embedding
from app.db.document_chunk_repository import search_similar_chunks
from app.services.generation_service import generate_answer


def _retrieve(query: str, top_k: int = 5):
    query_embedding = generate_query_embedding(query)
    return search_similar_chunks(query_embedding, top_k=top_k)


def search(query: str, top_k: int = 5):
    results = _retrieve(query, top_k)

    return [
        {
            "chunk_id": str(chunk.id),
            "document_id": str(chunk.document_id),
            "chunk_index": chunk.chunk_index,
            "text": chunk.chunk_text,
            "distance": distance,
        }
        for chunk, distance in results
    ]


def ask(query: str, top_k: int = 5) -> dict:
    results = _retrieve(query, top_k)

    context_chunks = [chunk.chunk_text for chunk, _ in results]
    answer = generate_answer(query, context_chunks)

    sources = [
        {
            "chunk_id": str(chunk.id),
            "document_id": str(chunk.document_id),
            "chunk_index": chunk.chunk_index,
            "distance": distance,
        }
        for chunk, distance in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
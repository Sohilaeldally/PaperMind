from app.services.embedding_service import generate_query_embedding
from app.db.document_chunk_repository import search_similar_chunks


def search(query: str, top_k: int = 5):
    query_embedding = generate_query_embedding(query)
    results = search_similar_chunks(query_embedding, top_k=top_k)

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
from uuid import UUID
from sentence_transformers import SentenceTransformer

from app.models.document import DocumentStatus
from app.db.document_repository import update_document_status
from app.db.document_chunk_repository import get_chunks_by_document_id, update_chunk_embedding

_model = SentenceTransformer("intfloat/multilingual-e5-small")


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    prefixed_chunks = [f"passage: {chunk}" for chunk in chunks]
    embeddings = _model.encode(prefixed_chunks, normalize_embeddings=True)
    return embeddings.tolist()


def process_embedding(document_id: UUID) -> None:
    chunks = get_chunks_by_document_id(document_id)
    if not chunks:
        raise ValueError(f"No chunks found for document: {document_id}")

    update_document_status(document_id, status=DocumentStatus.EMBEDDING)

    try:
        texts = [chunk.chunk_text for chunk in chunks]
        embeddings = generate_embeddings(texts)

        for chunk, embedding in zip(chunks, embeddings):
            update_chunk_embedding(chunk.id, embedding)

        update_document_status(document_id, status=DocumentStatus.COMPLETED)

    except Exception as e:
        update_document_status(document_id, status=DocumentStatus.FAILED, error_message=str(e))
        raise
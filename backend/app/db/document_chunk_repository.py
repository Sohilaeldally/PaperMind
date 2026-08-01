from uuid import UUID
from app.db.database import pool
from app.models.document_chunk import DocumentChunk


def insert_chunks(
    document_id: UUID,
    chunks: list[tuple[str, str]],
) -> list[DocumentChunk]:
    inserted_chunks = []

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            for index, (section_name, chunk_text) in enumerate(chunks):
                cursor.execute(
                    """
                    INSERT INTO document_chunks (id, document_id, chunk_index, chunk_text, section_name)
                    VALUES (gen_random_uuid(), %s, %s, %s, %s)
                    RETURNING id, document_id, chunk_index, chunk_text, section_name, created_at
                    """,
                    (document_id, index, chunk_text, section_name),
                )
                row = cursor.fetchone()
                inserted_chunks.append(
                    DocumentChunk(
                        id=row[0], document_id=row[1], chunk_index=row[2],
                        chunk_text=row[3], section_name=row[4], created_at=row[5],
                    )
                )

    return inserted_chunks


def get_chunks_by_document_id(document_id: UUID) -> list[DocumentChunk]:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, document_id, chunk_index, chunk_text, section_name, created_at
                FROM document_chunks
                WHERE document_id = %s
                ORDER BY chunk_index ASC
                """,
                (document_id,),
            )
            rows = cursor.fetchall()

    return [
        DocumentChunk(
            id=row[0], document_id=row[1], chunk_index=row[2],
            chunk_text=row[3], section_name=row[4], created_at=row[5],
        )
        for row in rows
    ]


def update_chunk_embedding(chunk_id: UUID, embedding: list[float]) -> None:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE document_chunks SET embedding = %s WHERE id = %s",
                (embedding, chunk_id),
            )


def search_similar_chunks(
    query_embedding: list[float],
    document_id: UUID | None = None,
    top_k: int = 5,
) -> list[tuple[DocumentChunk, float]]:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            if document_id is not None:
                cursor.execute(
                    """
                    SELECT id, document_id, chunk_index, chunk_text, section_name, created_at,
                           embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE embedding IS NOT NULL AND document_id = %s
                    ORDER BY distance ASC
                    LIMIT %s
                    """,
                    (str(query_embedding), document_id, top_k),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, document_id, chunk_index, chunk_text, section_name, created_at,
                           embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE embedding IS NOT NULL
                    ORDER BY distance ASC
                    LIMIT %s
                    """,
                    (str(query_embedding), top_k),
                )
            rows = cursor.fetchall()

    return [
        (
            DocumentChunk(
                id=row[0], document_id=row[1], chunk_index=row[2],
                chunk_text=row[3], section_name=row[4], created_at=row[5],
            ),
            row[6],
        )
        for row in rows
    ]
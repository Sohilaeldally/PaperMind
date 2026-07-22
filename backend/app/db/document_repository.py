from uuid import UUID
from app.db.database import pool
from app.models.document import Document, DocumentStatus


def insert_document(document: Document) -> Document:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (
                    id,
                    original_name,
                    stored_name,
                    content_type,
                    file_size,
                    status,
                    error_message
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, original_name, stored_name, content_type,
                          file_size, status, error_message, created_at, updated_at
                """,
                (
                    document.id,
                    document.original_name,
                    document.stored_name,
                    document.content_type,
                    document.file_size,
                    document.status.value,
                    document.error_message,
                ),
            )
            row = cursor.fetchone()

    return Document(
        id=row[0],
        original_name=row[1],
        stored_name=row[2],
        content_type=row[3],
        file_size=row[4],
        status=DocumentStatus(row[5]),
        error_message=row[6],
        created_at=row[7],
        updated_at=row[8],
    )


def get_document_by_id(document_id: UUID) -> Document | None:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, original_name, stored_name, content_type,
                       file_size, status, error_message, created_at, updated_at
                FROM documents
                WHERE id = %s
                """,
                (document_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Document(
                id=row[0],
                original_name=row[1],
                stored_name=row[2],
                content_type=row[3],
                file_size=row[4],
                status=DocumentStatus(row[5]),
                error_message=row[6],
                created_at=row[7],
                updated_at=row[8],
            )


def update_document_status(document_id: UUID, status: DocumentStatus, error_message: str | None = None) -> Document:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE documents
                SET status = %s, error_message = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, original_name, stored_name, content_type,
                          file_size, status, error_message, created_at, updated_at
                """,
                (status.value, error_message, document_id),
            )
            row = cursor.fetchone()

    return Document(
        id=row[0],
        original_name=row[1],
        stored_name=row[2],
        content_type=row[3],
        file_size=row[4],
        status=DocumentStatus(row[5]),
        error_message=row[6],
        created_at=row[7],
        updated_at=row[8],
    )


def get_all_documents() -> list[Document]:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, original_name, stored_name, content_type,
                       file_size, status, error_message, created_at, updated_at
                FROM documents
                ORDER BY created_at DESC
                """
            )
            rows = cursor.fetchall()

    return [
        Document(
            id=row[0],
            original_name=row[1],
            stored_name=row[2],
            content_type=row[3],
            file_size=row[4],
            status=DocumentStatus(row[5]),
            error_message=row[6],
            created_at=row[7],
            updated_at=row[8],
        )
        for row in rows
    ]
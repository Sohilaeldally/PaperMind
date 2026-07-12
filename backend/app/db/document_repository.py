from uuid import UUID
from app.db.database import pool
from app.models.document import Document


def insert_document(document: Document):
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
                """,
                (
                    document.id,
                    document.original_name,
                    document.stored_name,
                    document.content_type,
                    document.file_size,
                    document.status,
                    document.error_message,
                ),
            )
from uuid import UUID
from app.config.settings import settings   
from app.db.document_content_repository import get_document_content
from app.db.document_chunk_repository import insert_chunks
from app.db.document_repository import get_document_by_id, update_document_status
from app.models.document import DocumentStatus
from app.services.document_structure_service import chunk_document

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks





def process_chunking(document_id: UUID) -> None:
    document = get_document_by_id(document_id)
    if document is None:
        raise ValueError(f"Document not found: {document_id}")

    content = get_document_content(document_id)
    if content is None:
        raise ValueError(f"No content found for document: {document_id}")

    update_document_status(document_id, status=DocumentStatus.CHUNKING)

    try:
        file_path = settings.UPLOAD_DIR / document.stored_name   
        chunks = chunk_document(file_path, content.raw_text, document.content_type)  
        insert_chunks(document_id, chunks)
        update_document_status(document_id, status=DocumentStatus.CHUNKED)

    except Exception as e:
        update_document_status(document_id, status=DocumentStatus.FAILED, error_message=str(e))
        raise
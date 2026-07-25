from pathlib import Path
from uuid import UUID
from pypdf import PdfReader
from docx import Document as DocxDocument

from app.config.settings import settings
from app.models.document import DocumentStatus, DocumentType
from app.db.document_repository import get_document_by_id, update_document_status
from app.db.document_content_repository import insert_document_content


def _extract_from_pdf(file_path: Path) -> str:
    reader = PdfReader(file_path)
    text_parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(text_parts).strip()


def _extract_from_docx(file_path: Path) -> str:
    doc = DocxDocument(file_path)
    text_parts = [para.text for para in doc.paragraphs]
    return "\n".join(text_parts).strip()


def _extract_from_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


PARSERS = {
    DocumentType.PDF: _extract_from_pdf,
    DocumentType.DOCX: _extract_from_docx,
    DocumentType.TXT: _extract_from_txt,
}


def extract_text(file_path: Path, content_type: str) -> str:
    try:
        doc_type = DocumentType(content_type)
    except ValueError:
        raise ValueError(f"Unsupported content type for parsing: {content_type}")

    return PARSERS[doc_type](file_path)


def process_document(document_id: UUID) -> None:
    document = get_document_by_id(document_id)
    if document is None:
        raise ValueError(f"Document not found: {document_id}")

    update_document_status(document_id, status=DocumentStatus.PARSING)

    try:
        file_path = settings.UPLOAD_DIR / document.stored_name
        raw_text = extract_text(file_path, document.content_type)

        insert_document_content(document_id, raw_text)
        update_document_status(document_id, status=DocumentStatus.PARSED)

    except Exception as e:
        update_document_status(document_id, status=DocumentStatus.FAILED, error_message=str(e))
        raise
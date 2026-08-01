from uuid import UUID
from fastapi import APIRouter, HTTPException,UploadFile, File,background_tasks
from app.services.document_service import save_uploaded_file
from app.services.parser_service import process_document
from app.services.chunking_service import process_chunking
from app.services.embedding_service import process_embedding
from app.db.document_repository import get_all_documents,get_document_by_id


router = APIRouter(prefix="/documents", tags=["Documents"])

def process_full_pipeline(document_id: UUID) -> None:
    try:
        process_document(document_id)
        process_chunking(document_id)
        process_embedding(document_id)
    except Exception:
        pass


@router.post("/upload")
async def upload_document(file: UploadFile, background_tasks: BackgroundTasks):
    new_doc = await save_uploaded_file(file)

    background_tasks.add_task(process_full_pipeline, new_doc.id)

    return {
        "message": "File uploaded successfully. Your document is being processed.",
        "id": str(new_doc.id),
        "original_name": new_doc.original_name,
        "stored_name": new_doc.stored_name,
    }

@router.get("/")
async def list_documents():
    documents = get_all_documents()
    return [
        {
            "id": str(doc.id),
            "original_name": doc.original_name,
            "status": doc.status.value,
            "error_message": doc.error_message,
            "file_size": doc.file_size,
            "created_at": doc.created_at,
        }
        for doc in documents
    ]


@router.get("/{document_id}")
async def get_document(document_id: UUID):
    document = get_document_by_id(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": str(document.id),
        "original_name": document.original_name,
        "status": document.status.value,
        "error_message": document.error_message,
        "file_size": document.file_size,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
    }
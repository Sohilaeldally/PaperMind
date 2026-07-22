from fastapi import APIRouter, HTTPException,UploadFile, File
from app.services.document_service import save_uploaded_file
from app.services.parser_service import process_document
from app.services.chunking_service import process_chunking
from app.services.embedding_service import process_embedding
from app.db.document_repository import get_all_documents,get_document_by_id

from uuid import UUID

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
   new_doc = await save_uploaded_file(file)
  
   try:
        process_document(new_doc.id)
        process_chunking(new_doc.id)
        process_embedding(new_doc.id)
   except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"File uploaded but parsing failed: {str(e)}"
        )

   return {
            "message": "File uploaded successfully and metadata saved.",
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
        

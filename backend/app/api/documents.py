from fastapi import APIRouter, HTTPException,UploadFile, File
from app.services.document_service import save_uploaded_file
from app.services.parser_service import process_document
from app.services.chunking_service import process_chunking
from app.services.embedding_service import process_embedding

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

        

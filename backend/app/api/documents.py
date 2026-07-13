from fastapi import APIRouter,UploadFile, File
from app.services.document_service import save_uploaded_file

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
   new_doc = await save_uploaded_file(file)
   return {
            "message": "File uploaded successfully and metadata saved.",
            "id": str(new_doc.id),
            "original_name": new_doc.original_name, 
            "stored_name": new_doc.stored_name,
        }
  
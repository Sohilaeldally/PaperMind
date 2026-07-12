from fastapi import HTTPException
ALLOWED_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

ALLOWED_SIZE_MB= 10

def validate_file_type(content_type: str):
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,detail="Unsupported file type. Allowed types are: PDF, TXT, MD, DOCX.")

def validate_file_size(file_size: int):
    if file_size > ALLOWED_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File size exceeds the limit of {ALLOWED_SIZE_MB} MB.")
    


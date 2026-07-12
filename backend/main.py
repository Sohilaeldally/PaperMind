from fastapi import FastAPI
from app.api.documents import router as documents_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to DocMind-AI!"}

app.include_router(documents_router)


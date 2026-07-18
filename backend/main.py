from fastapi import FastAPI
from app.api.documents import router as documents_router
from app.api.search import router as search_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to DocMind-AI!"}

app.include_router(documents_router)
app.include_router(search_router)

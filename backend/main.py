from fastapi import FastAPI

from backend.database import engine, Base
from backend.models.user import User

from backend.routers import auth
from backend.routers import documents
from backend.models.document import Document

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DocuMind",
    description="AI powered document assistant",
    version="0.1.0"
)

app.include_router(auth.router)
app.include_router(documents.router)


@app.get("/")
async def home():
    return {
        "message": "DocuMind is alive 🚀",
        "version": "0.1.0"
    }
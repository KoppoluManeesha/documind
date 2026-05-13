from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from backend.routers import auth
from backend.routers import documents
from backend.database import Base, engine
from backend.models.user import User
from backend.models.document import Document
Base.metadata.create_all(bind=engine)
from backend.exceptions import (
    DocuMindException,
    documind_exception_handler,
    validation_exception_handler,
    integrity_exception_handler
)

app = FastAPI(
    title="DocuMind",
    description="AI powered document assistant",
    version="0.1.0"
)

# CORS — allow React frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(DocuMindException, documind_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)

# Register routers
app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/")
async def home():
    return {
        "message": "DocuMind is alive",
        "version": "0.1.0",
        "docs": "Visit /docs to see all API endpoints"
    }
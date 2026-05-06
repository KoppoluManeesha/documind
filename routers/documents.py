from fastapi import APIRouter
from schemas.document import DocumentCreate, DocumentResponse
from datetime import datetime

# APIRouter is like Django's urls.py
# It groups all document-related routes together
# prefix means all routes here start with /documents
router = APIRouter(
    prefix="/documents",
    tags=["Documents"]  # this groups them nicely in /docs page
)

# Temporary in-memory storage — like a fake database
# On Day 3 we replace this with real PostgreSQL
fake_db = []
document_counter = 1

# ============================================
# Route 1 — Create a new document
# POST /documents/
# ============================================
@router.post("/", response_model=DocumentResponse)
async def create_document(document: DocumentCreate):
    global document_counter

    # Simulate saving to database
    new_document = {
        "id": document_counter,
        "title": document.title,
        "content": document.content,
        "description": document.description,
        "uploaded_at": datetime.now(),
        "is_active": True
    }

    fake_db.append(new_document)
    document_counter += 1

    return new_document

# ============================================
# Route 2 — Get all documents
# GET /documents/
# ============================================
@router.get("/", response_model=list[DocumentResponse])
async def get_all_documents():
    return fake_db

# ============================================
# Route 3 — Get a single document by ID
# GET /documents/1
# ============================================
@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int):
    for doc in fake_db:
        if doc["id"] == document_id:
            return doc
    # If not found — we will improve this on Day 2
    return {"error": "Document not found"}
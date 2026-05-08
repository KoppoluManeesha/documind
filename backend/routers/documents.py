from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from backend.ai import analyze_document

from backend.database import get_db
from backend.auth import get_current_user

from backend.models.user import User
from backend.models.document import Document

from backend.schemas.document import (
    DocumentCreate,
    DocumentResponse
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/",
    response_model=DocumentResponse
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_document = Document(
        title=document.title,
        content=document.content,
        owner_id=current_user.id
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    documents = db.query(Document).filter(
        Document.owner_id == current_user.id
    ).all()

    return {
        "user": current_user.email,
        "documents": documents
    }
@router.post("/{document_id}/analyze")
def analyze_user_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find document
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()

    # Check ownership
    if not document:
        return {
            "error": "Document not found"
        }

    # AI analysis
    analysis = analyze_document(
        document.content
    )

    return {
        "document": document.title,
        "analysis": analysis
    }
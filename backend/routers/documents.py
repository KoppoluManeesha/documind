from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models.document import Document
from backend.dependencies import get_current_user
from backend.ai import ask_document_ai

router = APIRouter()

class DocumentCreate(BaseModel):
    title: str
    content: str

@router.post("/documents")
def create_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_document = Document(
        title=doc.title,
        content=doc.content,
        user_id=current_user.id
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@router.post("/documents/{doc_id}/analyze")
def analyze_user_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    analysis = ask_document_ai(
        document.content,
        "Summarize this document"
    )

    return {
        "document_title": document.title,
        "analysis": analysis
    }
from sqlalchemy.orm import Session
from backend.models.document import Document
from backend.schemas.document import DocumentCreate
from exceptions import DocuMindException
from fastapi import status

def create_document(db: Session, document: DocumentCreate, user_id: int) -> Document:
    new_document = Document(
        title=document.title,
        content=document.content,
        description=document.description,
        user_id=user_id,
        is_active=True
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

def get_all_documents(db: Session, user_id: int) -> list[Document]:
    return db.query(Document)\
             .filter(Document.user_id == user_id)\
             .filter(Document.is_active == True)\
             .all()

def get_document_by_id(db: Session, document_id: int, user_id: int) -> Document:
    document = db.query(Document)\
                 .filter(Document.id == document_id)\
                 .filter(Document.user_id == user_id)\
                 .filter(Document.is_active == True)\
                 .first()
    if not document:
        raise DocuMindException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Document not found",
            details=f"No document with id {document_id} belongs to you"
        )
    return document

def delete_document(db: Session, document_id: int, user_id: int) -> Document:
    document = get_document_by_id(db, document_id, user_id)
    document.is_active = False
    db.commit()
    db.refresh(document)
    return document
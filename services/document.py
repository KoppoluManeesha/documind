from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate

# ============================================
# CREATE — saves a new document to database
# ============================================
def create_document(db: Session, document: DocumentCreate) -> Document:
    # Create a new SQLAlchemy model instance
    # This is like filling in a form before filing it
    new_document = Document(
        title=document.title,
        content=document.content,
        description=document.description,
        is_active=True
    )

    db.add(new_document)      # add to session — like putting form in inbox
    db.commit()               # save to database permanently — like filing it
    db.refresh(new_document)  # get updated data back — like reading the filed copy
    return new_document

# ============================================
# GET ALL — fetches all active documents
# ============================================
def get_all_documents(db: Session) -> list[Document]:
    return db.query(Document)\
             .filter(Document.is_active == True)\
             .all()

# ============================================
# GET ONE — fetches a single document by ID
# ============================================
def get_document_by_id(db: Session, document_id: int) -> Document | None:
    return db.query(Document)\
             .filter(Document.id == document_id)\
             .filter(Document.is_active == True)\
             .first()

# ============================================
# DELETE — soft delete, never removes from database
# ============================================
def delete_document(db: Session, document_id: int) -> Document | None:
    document = get_document_by_id(db, document_id)
    if not document:
        return None
    document.is_active = False  # soft delete
    db.commit()
    db.refresh(document)
    return document
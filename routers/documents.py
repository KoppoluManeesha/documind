from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.document import DocumentCreate, DocumentResponse, DocumentListResponse
from services import document as document_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ============================================
# CREATE document
# POST /documents/
# ============================================
@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED  # 201 = created, more accurate than 200
)
async def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)  # FastAPI injects database session automatically
):
    return document_service.create_document(db=db, document=document)

# ============================================
# GET ALL documents
# GET /documents/
# ============================================
@router.get("/", response_model=DocumentListResponse)
async def get_all_documents(db: Session = Depends(get_db)):
    documents = document_service.get_all_documents(db=db)
    return DocumentListResponse(
        total=len(documents),
        documents=documents
    )

# ============================================
# GET ONE document
# GET /documents/1
# ============================================
@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = document_service.get_document_by_id(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )
    return document

# ============================================
# DELETE document
# DELETE /documents/1
# ============================================
@router.delete("/{document_id}", response_model=DocumentResponse)
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = document_service.delete_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )
    return document
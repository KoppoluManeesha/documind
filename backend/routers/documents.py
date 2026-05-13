from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models.document import Document
from backend.dependencies import get_current_user
from backend.ai import ask_document_ai
import shutil
import os
import PyPDF2

router = APIRouter()

@router.get("/documents")
def get_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    docs = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()
    return docs

class DocumentCreate(BaseModel):
    title: str
    content: str

class QuestionRequest(BaseModel):
    prompt: str

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

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    os.makedirs("uploads", exist_ok=True)

    if file.filename.endswith(".txt"):
        file_content = file.file.read().decode("utf-8")
    elif file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        file_content = ""
        for page in reader.pages:
            file_content += (page.extract_text() or "") + "\n"
        file_content = file_content.replace(" — ", "\n").replace("—", "\n").replace("|", "\n")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    file.file.seek(0)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_doc = Document(
        filename=file.filename,
        content=file_content,
        user_id=current_user.id
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "message": "File uploaded successfully",
        "document": new_doc
    }

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
        raise HTTPException(status_code=404, detail="Document not found")

    analysis = ask_document_ai(document.content, "Summarize this document")

    return {
        "document_title": document.title,
        "analysis": analysis
    }

@router.post("/analyze/{doc_id}")
def analyze_document(
    doc_id: int,
    body: QuestionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    analysis = ask_document_ai(doc.content, body.prompt)

    return {"analysis": analysis}

@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(doc)
    db.commit()

    return {"message": "Document deleted successfully"}
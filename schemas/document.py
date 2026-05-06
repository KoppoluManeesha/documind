from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ============================================
# Used when USER SENDS data to us
# ============================================
class DocumentCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Title of the document"
    )
    content: str = Field(
        min_length=10,
        description="Main content of the document"
    )
    description: Optional[str] = None

# ============================================
# Used when WE SEND data back to user
# ============================================
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    description: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    is_active: bool

    # This tells Pydantic to read data from
    # SQLAlchemy model attributes directly
    model_config = {"from_attributes": True}

# ============================================
# Used when returning a list of documents
# ============================================
class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentResponse]
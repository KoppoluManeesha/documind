from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ============================================
# This schema is used when USER SENDS data to us
# Think — what does the user fill in when uploading a document?
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
# This schema is used when WE SEND data back to user
# Think — what does the user see after uploading?
# ============================================
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    description: Optional[str] = None
    uploaded_at: datetime
    is_active: bool

    # This tells Pydantic to work with SQLAlchemy models
    # You will understand this fully on Day 3 when we add the database
    model_config = {"from_attributes": True}
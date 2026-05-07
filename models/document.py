from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
    file_size_mb = Column(Float, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # ForeignKey — links each document to its owner
    # Like Django's ForeignKey(User, on_delete=CASCADE)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship — lets you do document.owner to get the user object
    owner = relationship("User", back_populates="documents")

    def __repr__(self):
        return f"<Document id={self.id} title={self.title}>"
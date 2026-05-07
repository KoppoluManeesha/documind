from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Email is the username — must be unique
    # No two users can have the same email
    email = Column(String(255), unique=True, nullable=False, index=True)
    
    # Full name — optional
    full_name = Column(String(255), nullable=True)
    
    # NEVER store plain password
    # Always store the hashed version
    # bcrypt hash looks like: $2b$12$... 
    hashed_password = Column(String(255), nullable=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship — one user has many documents
    # This is like Django's ForeignKey reverse relation
    # lazy="dynamic" means don't load documents until asked
    documents = relationship("Document", back_populates="owner")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
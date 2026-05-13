from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base



class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=True)
    content = Column(String(5000), nullable=True)

    filename = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
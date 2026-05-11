from fastapi import Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User


def get_current_user(
    db: Session = Depends(get_db)
):
    user = db.query(User).first()
    return user
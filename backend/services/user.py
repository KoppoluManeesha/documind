from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.auth import hash_password, verify_password

def create_user(db: Session, user: UserCreate) -> User:
    # Hash the password before saving
    # Never save plain text password
    hashed = hash_password(user.password)
    
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    # Step 1 — find user by email
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    # Step 2 — verify password
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
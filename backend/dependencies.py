# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from config import SECRET_KEY, ALGORITHM

# This tells FastAPI: "look for a Bearer token in the Authorization header"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    
    # Define the error we'll raise if anything goes wrong
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract email from the token payload
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        # Token is invalid or expired — raise 401
        raise credentials_exception

    # Look up the user in the database
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise credentials_exception

    return user  # ✅ Route gets this user object
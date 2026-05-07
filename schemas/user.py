from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Used when user REGISTERS
class UserCreate(BaseModel):
    email: EmailStr  # EmailStr validates email format automatically
    full_name: Optional[str] = None
    password: str = Field(min_length=8, description="Minimum 8 characters")

# Used when returning user data — never include password
class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

# Used for login form
class UserLogin(BaseModel):
    email: str
    password: str

# Used for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Used inside JWT token
class TokenData(BaseModel):
    email: Optional[str] = None
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    middle_name: str | None = None

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None  = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
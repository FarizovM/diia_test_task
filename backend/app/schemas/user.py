from pydantic import BaseModel, EmailStr
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True

class Permission(str, Enum):
    EDIT_TASK = "edit_task"
    DELETE_TASK = "delete_task"
    EDIT_USER = "edit_user"
    DELETE_USER = "delete_user"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    permissions: list[Permission] = []
from pydantic import BaseModel, EmailStr, field_validator
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    middle_name: str | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль повинен містити щонайменше 8 символів")
        if len(v) > 128:
            raise ValueError("Пароль не повинен перевищувати 128 символів")
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("Пароль повинен містити хоча б одну латинську літеру")
        if not re.search(r"\d", v):
            raise ValueError("Пароль повинен містити хоча б одну цифру")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Поле не може бути порожнім")
        return v.strip()

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
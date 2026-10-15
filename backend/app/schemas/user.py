from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re

class UserCreate(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Електронна пошта користувача (використовується для входу в систему)",
        examples=["user@diia.gov.ua"]
    )
    password: str = Field(
        ...,
        description="Пароль для облікового запису (від 8 до 128 символів, обов'язково містить латинські літери та цифри)",
        min_length=8,
        max_length=128,
        examples=["SecurePass123!"]
    )
    first_name: str = Field(
        ...,
        description="Ім'я користувача",
        min_length=1,
        max_length=100,
        examples=["Тарас"]
    )
    last_name: str = Field(
        ...,
        description="Прізвище користувача",
        min_length=1,
        max_length=100,
        examples=["Шевченко"]
    )
    middle_name: str | None = Field(
        None,
        description="По батькові користувача (необов'язкове поле)",
        max_length=100,
        examples=["Григорович"]
    )

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
    user_id: str = Field(
        ...,
        description="Унікальний ідентифікатор користувача (UUIDv4)",
        examples=["4a87c12e-9d22-482d-83b6-71d532a832c7"]
    )
    email: EmailStr = Field(
        ...,
        description="Електронна пошта користувача",
        examples=["user@diia.gov.ua"]
    )
    first_name: str = Field(
        ...,
        description="Ім'я користувача",
        examples=["Тарас"]
    )
    last_name: str = Field(
        ...,
        description="Прізвище користувача",
        examples=["Шевченко"]
    )
    middle_name: str | None = Field(
        None,
        description="По батькові користувача",
        examples=["Григорович"]
    )
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str = Field(
        ...,
        description="Підписаний JWT токен для авторизації запитів (Bearer)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(
        default="bearer",
        description="Тип токена авторизації (за замовчуванням 'bearer')",
        examples=["bearer"]
    )
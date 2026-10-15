from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Отримання профілю поточного користувача",
    description="Повертає повну інформацію про поточного автентифікованого користувача (ID, email, ім'я, прізвище та по батькові) за переданим Bearer-токеном.",
    response_description="Профіль авторизованого користувача",
    responses={
        200: {"description": "Профіль успішно отримано"},
        401: {"description": "Неавторизований доступ, недійсний токен або термін його дії минув"}
    }
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
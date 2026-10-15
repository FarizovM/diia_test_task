from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from redis.asyncio import Redis

from app.db.database import get_db
from app.db.redis import get_redis
from app.db.models import User

from app.schemas.user import UserCreate, UserResponse, Token

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.logger import logger

from app.api.dependencies import get_current_user, oauth2_scheme


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Реєстрація нового користувача",
    description="Створює новий обліковий запис у системі. Пароль проходить обов'язкову валідацію на складність та безпечно хешується за допомогою bcrypt.",
    response_description="Дані успішно зареєстрованого користувача",
    responses={
        400: {"description": "Користувач із зазначеним email вже існує або пароль не відповідає політиці безпеки"},
        422: {"description": "Помилка валідації вхідного тіла запиту"}
    }
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    
    logger.info(f"Спроба реєстрації нового користувача - {user_in.email}")

    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        logger.error(f"Користувач з email {user_in.email} вже існує")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Створюємо нового користувача з хешованим паролем
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        middle_name=user_in.middle_name,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    logger.info(f"Новий користувач зареєстрований: {UserResponse.model_validate(new_user).model_dump_json()}")
    
    return new_user

@router.post(
    "/login",
    response_model=Token,
    summary="Авторизація та отримання JWT токена",
    description="Автентифікація користувача за стандартом OAuth2 Password Request. У полі 'username' необхідно передавати email користувача. Повертає підписаний JWT Bearer токен для подальших запитів.",
    response_description="Access токен з типом 'bearer'",
    responses={
        401: {"description": "Невірний логін (email) або пароль"},
        422: {"description": "Помилка валідації вхідної форми"}
    }
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    
    logger.info(f"Спроба входу користувача - {form_data.username}")

    # У OAuth2PasswordRequestForm поле називається username, але ми передаємо туди email
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    # Перевірка наявності користувача та правильності пароля
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.error(f"Користувач з email {form_data.username} не існує або пароль невірний")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.user_id})
    
    logger.info(f"Користувач {user.user_id} успішно авторизований. Токен створено")
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/logout",
    summary="Вихід із системи (анулювання токена)",
    description="Анулює діючий JWT токен авторизованого користувача шляхом додавання його до чорного списку (Redis Blacklist) на час дії його TTL, унеможливлюючи його повторне використання.",
    response_description="Підтвердження успішного завершення сесії",
    responses={
        200: {"description": "Сесію успішно завершено, токен додано до чорного списку"},
        401: {"description": "Неавторизований доступ, недійсний або вже відкликаний токен"}
    }
)
async def logout(
    token: str = Depends(oauth2_scheme),
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis)
):
    ttl = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    
    # Додаємо токен у чорний список (Blacklist) в Redis з префіксом bl_
    await redis.setex(f"bl_{token}", ttl, "true")
    
    logger.info(f"Користувач {current_user.user_id} успішно вийшов з системи. Токен додано до чорного списку")

    return {"message": "Successfully logged out"}
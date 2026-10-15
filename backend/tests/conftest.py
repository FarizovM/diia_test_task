import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.models import Base, User
from app.db.database import get_db
from app.db.redis import get_redis
from app.core.security import get_password_hash, create_access_token

# Тестова БД в оперативній пам'яті (не потребує запущеного Postgres)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionTest = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

class FakeRedis:
    """Мок для Redis, щоб тестувати логаут та blacklist без реального Redis"""
    def __init__(self):
        self.store = {}

    async def get(self, key: str):
        return self.store.get(key)

    async def setex(self, key: str, ttl: int, value: str):
        self.store[key] = value
        return True

fake_redis = FakeRedis()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionTest() as session:
        yield session

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    fake_redis.store.clear()

    async def override_get_db():
        yield db_session

    async def override_get_redis():
        yield fake_redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def auth_headers(db_session: AsyncSession) -> dict:
    """Створює тестового користувача і повертає заголовок Authorization з JWT"""
    user = User(
        email="unit_test@diia.gov.ua",
        hashed_password=get_password_hash("testpass123"),
        first_name="Тест",
        last_name="Користувач"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(data={"sub": user.user_id})
    return {"Authorization": f"Bearer {token}"}
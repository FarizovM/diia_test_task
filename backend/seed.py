import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select

from app.db.database import async_session_maker
from app.db.models import User, Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash


async def seed():
    print("🌱 Starting database seeding...")
    async with async_session_maker() as session:

        email = "test@diia.gov.ua"
        password = "password123"

        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            user = User(
                user_id=str(uuid.uuid4()),
                email=email,
                hashed_password=get_password_hash(password),
                first_name="Адміністратор",
                last_name="Дія",
                middle_name="Тестовий",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            print(f"✅ Created user: {user.email} (Password: {password})")
        else:
            # Оновлюємо хеш пароля на випадок, якщо він був змінений
            user.hashed_password = get_password_hash(password)
            user.updated_at = datetime.now(timezone.utc)
            await session.commit()
            print(f"ℹ️ User {user.email} already exists (Password confirmed: {password})")

        tasks_result = await session.execute(select(Task).where(Task.created_by == user.user_id))
        existing_tasks = {task.title for task in tasks_result.scalars().all()}

        now = datetime.now(timezone.utc)

        tasks_data = [
            {
                "title": "Інтеграція з сервісом Дія.Підпис",
                "description": "Реалізувати ендпоінт для верифікації цифрового підпису користувача та валідації сертифікатів.",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGHEST,
                "deadline": now + timedelta(days=3),
            },
            {
                "title": "Налаштування автентифікації через BankID",
                "description": "Підключити NBU BankID провайдер для спрощеної авторизації громадян.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.HIGH,
                "deadline": now + timedelta(days=7),
            },
            {
                "title": "Оптимізація SQL-запитів до реєстру завдань",
                "description": "Додати композитні індекси та проаналізувати EXPLAIN ANALYZE для повільних вибірок.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.HIGH,
                "deadline": now - timedelta(days=2),
            },
            {
                "title": "Аудит безпеки сесій та Redis токенів",
                "description": "Перевірити валідність збереження blacklist-токенів у Redis та коректність їх TTL.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.MEDIUM,
                "deadline": now - timedelta(days=5),
            },
            {
                "title": "Створення UI компонентів фільтрації та сортування",
                "description": "Розробити випадаючі списки для фільтрації за пріоритетом, статусом та дедлайном у Vue 3.",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "deadline": now + timedelta(days=2),
            },
            {
                "title": "Реалізація пагінації для списку завдань",
                "description": "Додати параметри page та limit на бекенді та компонент пагінатора у таблиці на фронтенді.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.MEDIUM,
                "deadline": now - timedelta(days=1),
            },
            {
                "title": "Розробка форми створення нового завдання",
                "description": "Створити модальне вікно з валідацією полів: назва, опис, пріоритет та дедлайн.",
                "status": TaskStatus.QA,
                "priority": TaskPriority.HIGH,
                "deadline": now + timedelta(days=1),
            },
            {
                "title": "Налаштування сповіщень про наближення дедлайну",
                "description": "Створити фоновий воркер для відправки email-нагадувань за 24 години до настання дедлайну.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
                "deadline": now + timedelta(days=10),
            },
            {
                "title": "Покриття unit-тестами модулів аутентифікації",
                "description": "Написати pytest тести для /auth/register, /auth/login та /auth/logout.",
                "status": TaskStatus.QA,
                "priority": TaskPriority.HIGH,
                "deadline": now + timedelta(days=4),
            },
            {
                "title": "Рефакторинг обробки помилок у FastAPI",
                "description": "Додати глобальний exception handler для стандартизації JSON-відповідей помилок.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.LOW,
                "deadline": now - timedelta(days=10),
            },
            {
                "title": "Адаптація інтерфейсу під мобільні пристрої",
                "description": "Забезпечити адаптивне відображення карток завдань, модалок та меню на мобільних екранах.",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.MEDIUM,
                "deadline": now + timedelta(days=5),
            },
            {
                "title": "Додавання темної теми (Dark Mode)",
                "description": "Налаштувати перемикач теми та конфігурацію Tailwind CSS для підтримки темного режиму.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOWEST,
                "deadline": now + timedelta(days=20),
            },
            {
                "title": "Експорт списку завдань у формат CSV/Excel",
                "description": "Реалізувати можливість завантаження відфільтрованого переліку задач у файл CSV.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "deadline": now + timedelta(days=15),
            },
            {
                "title": "Оновлення документації Swagger та OpenAPI",
                "description": "Додати детальні описи схем, приклади тіла запитів та відповідей для всіх роутів.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.LOWEST,
                "deadline": now - timedelta(days=3),
            },
            {
                "title": "Перевірка валідації дат у дедлайнах",
                "description": "Заборонити встановлення дедлайну в минулому часі через валідатор у Pydantic схемі.",
                "status": TaskStatus.QA,
                "priority": TaskPriority.MEDIUM,
                "deadline": now + timedelta(days=3),
            },
            {
                "title": "Налаштування Docker Healthcheck",
                "description": "Додати перевірку стану для сервісів backend, postgres та redis у docker-compose.yml.",
                "status": TaskStatus.DONE,
                "priority": TaskPriority.LOW,
                "deadline": now - timedelta(days=4),
            },
            {
                "title": "Інтеграційне тестування життєвого циклу задачі",
                "description": "Протестувати сценарій: Створення -> Редагування -> Зміна статусу -> Видалення.",
                "status": TaskStatus.IN_PROGRESS,
                "priority": TaskPriority.HIGH,
                "deadline": now + timedelta(days=6),
            },
            {
                "title": "Впровадження Rate Limiting для публічних ендпоінтів",
                "description": "Обмежити кількість запитів на вхід за допомогою Redis для захисту від brute-force атак.",
                "status": TaskStatus.FLAGGED,
                "priority": TaskPriority.HIGHEST,
                "deadline": now + timedelta(days=8),
            },
            {
                "title": "Очищення застарілих задач у статусі Done",
                "description": "Розробити механізм архівування або м'якого видалення (soft delete) для завершених завдань.",
                "status": TaskStatus.TODO,
                "priority": TaskPriority.LOW,
                "deadline": None,
            },
            {
                "title": "Оптимізація збірки фронтенду через Vite",
                "description": "Налаштувати code-splitting та оптимізувати розмір фінального JavaScript бандлу.",
                "status": TaskStatus.QA,
                "priority": TaskPriority.LOW,
                "deadline": now + timedelta(days=12),
            },
        ]

        created_count = 0
        for i, data in enumerate(tasks_data):
            if data["title"] not in existing_tasks:
                task_time = now - timedelta(minutes=(len(tasks_data) - i) * 10)
                task = Task(
                    task_id=str(uuid.uuid4()),
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    deadline=data["deadline"],
                    created_by=user.user_id,
                    updated_by=user.user_id,
                    created_at=task_time,
                    updated_at=task_time,
                )
                session.add(task)
                created_count += 1

        await session.commit()
        print(f"✅ Created {created_count} new tasks (total in dataset: {len(tasks_data)}).")
        print("🎉 Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed())

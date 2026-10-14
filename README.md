# Task Manager (Test Task)

Цей проєкт є виконанням тестового завдання на позицію Full Stack розробника (Python + Vue.js). 
Система є API для управління задачами з додатковим фокусом на безпеку, кешування та мікросервісну архітектуру.

## 🚀 Технологічний стек
* **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async), Alembic, Pydantic, JWT (PyJWT), Passlib
* **Frontend:** Vue.js 3, Vite, Tailwind CSS (в процесі налаштування)
* **Бази даних:** PostgreSQL (основна БД), Redis (для кешування та Blacklist-токенів сесій)
* **Інфраструктура:** Docker, Docker Compose

## 📋 Передумови
Для запуску проєкту на новому комп'ютері вам знадобиться лише:
* Встановлений [Docker Desktop](https://www.docker.com/products/docker-desktop/) (або Docker Engine + Docker Compose).
* Git (для завантаження репозиторію).

---

## 🛠 Інструкція з локального запуску

### 1. Клонування репозиторію
Стягніть проєкт на ваш комп'ютер та перейдіть у його кореневу папку:
```bash
git clone <посилання_на_ваш_репозиторій>
cd diia_test_task
```
### 2. Запуск контейнерів
Зберіть та запустіть усі сервіси (PostgreSQL, Redis, Backend, Frontend) у фоновому режимі:
```bash
docker-compose up --build -d
```
Зачекайте кілька секунд, щоб база даних повністю ініціалізувалась.

### 3. Застосування міграцій бази даних
Створіть необхідні таблиці в PostgreSQL, виконавши міграції Alembic всередині контейнера бекенду:

```bash
docker exec -it task_manager_backend alembic upgrade head
```

### 4. Генерація тестових даних (Seeding)
Щоб не створювати користувачів та задачі вручну, запустіть скрипт, який згенерує тестового адміністратора та 20 задач (для перевірки пагінації та фільтрів):

```bash
docker exec -it task_manager_backend python seed.py
```

### 🌐 Доступ до сервісів

Після успішного запуску, сервіси будуть доступні за наступними адресами:

- Backend API (Swagger UI): http://localhost:8000/docs — Тут можна протестувати всі ендпоінти API.
- Frontend (UI): http://localhost:3000

### 🔐 Тестові дані для входу

Якщо ви виконали крок 4 (Seeding), використовуйте ці дані для авторизації в Swagger (кнопка Authorize) або на фронтенді:

- Email: test@diia.gov.ua
- Password: password123

### 🛑 Управління проєктом

Перегляд логів бекенду в реальному часі:

```bash
docker-compose logs -f backend
```
Зупинка всіх контейнерів:

```bash
docker-compose down
```
Зупинка та видалення даних (контейнери + мережа, але не томи з БД):

```bash
docker-compose down -v
```
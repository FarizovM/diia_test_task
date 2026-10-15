# Трембіта CRM — Task Manager (Test Task)

Сучасна повнофункціональна система управління завданнями (**Full Stack: FastAPI + Vue 3**), розроблена в межах тестового завдання. Проєкт побудований за концепцією **Low-Code реєстрів (Config-driven UI)** та виконаний у фірмовій дизайн-системі **Дія**.

---

## 🚀 Технологічний стек

### **Backend**
* **Мова та фреймворк:** Python 3.11, FastAPI (асинхронна архітектура)
* **ORM та БД:** SQLAlchemy 2 (Asyncio + `asyncpg`), PostgreSQL 15
* **Міграції:** Alembic
* **Кешування та безпека:** Redis 7 (кешування та Blacklist JWT-токенів при виході)
* **Автентифікація:** JWT (PyJWT), Passlib (Bcrypt)
* **Валідація:** Pydantic v2 (Pydantic Settings, EmailStr)

### **Frontend**
* **Фреймворк:** Vue.js 3 (Composition API, `<script setup lang="ts">`)
* **Типізація:** TypeScript (строгий режим `vue-tsc`)
* **Збірка:** Vite
* **Стилізація:** Tailwind CSS 3, дизайн-система **Дія** (`#1C1C1E`, `#F5F5F7`, `#C6F150`)
* **Стейт-менеджмент:** Pinia
* **Маршрутизація:** Vue Router 4 (з Navigation Guards для захисту маршрутів)
* **HTTP-клієнт:** Axios (інтерцептори для автоматичного підставлення Bearer токена)

### **Інфраструктура**
* **Контейнеризація:** Docker, docker-compose (мультиконтейнерне середовище: `db`, `redis`, `backend`, `frontend`)

---

## ✨ Ключовий функціонал системи

1. 🔐 **Повноцінна автентифікація та профіль користувача**:
   * Реєстрація з введенням повних даних (Прізвище, Ім'я, По батькові, Email, Пароль).
   * Авторизація за JWT-токеном (OAuth2 Password Bearer).
   * Безпечний вихід (`/auth/logout`) з додаванням активного токена у **Redis Blacklist**.
   * Відображення ПІБ та email користувача у бічній панелі.

2. 📊 **Аналітична панель моніторингу (`/about`)**:
   * Динамічні картки ключових показників (KPI): «Всього задач», «В процесі», «На QA», «Виконано», «Заблоковано», «Прострочено».
   * Режими перегляду: **Порівняння** (Загальні vs Мої задачі), **Загальна система**, **Мої задачі**.
   * Графіки розподілу за статусами та пріоритетами, контроль прострочених дедлайнів.

3. 📑 **Low-Code Реєстр задач (`/tasks`)**:
   * **Config-driven архітектура** (`tasksRegistry.ts`): конфігурація колонок, типи даних (`text`, `textarea`, `select`, `badge`, `date`, `number`), плейсхолдери, сортування та обов'язковість.
   * **Кастомний компонент випадалок (`RegistrySelect`)**: замінює нативний браузерний select на фірмовий Дія-дропдаун з іконками та бейджами класифікаторів. Використовується як у фільтрах, так і у формах.
   * **Кастомний компонент календаря (`RegistryDatePicker`)**: локалізований вибір дати та часу (години/хвилини, пресети `09:00`, `13:00`, `18:00`, `23:59`) з адаптивним відкриттям.
   * **Універсальна таблиця**: серверний пошук, комбінована фільтрація за статусом і пріоритетом, клікабельне сортування за колонками.
   * **Повний CRUD**: створення та редагування задач у модальному вікні, підтвердження видалення (`RegistryDeleteModal`), реактивні тост-сповіщення (`RegistryToast`).
   * **Пагінація (`RegistryPagination`)**: вибір кількості рядків на сторінці (10, 25, 50, 100), навігація по сторінках.

---

## 📁 Структура проєкту

```text
diia_test_task/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/          # Маршрути: auth, tasks, stats, users
│   │   │   └── dependencies.py  # Інжекція сесій БД, Redis, поточного юзера
│   │   ├── core/                # Конфігурація (Pydantic Settings), безпека (JWT, hashing)
│   │   ├── db/                  # Підключення до asyncpg, Redis, моделі SQLAlchemy
│   │   ├── schemas/             # Pydantic схеми (Task, User, Stats, Token)
│   │   └── main.py              # Точка входу FastAPI додатку
│   ├── migrations/              # Alembic міграції бази даних
│   ├── requirements.txt         # Python залежності
│   ├── seed.py                  # Скрипт генерації тестових даних
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                 # Axios інстанс з інтерцепторами
│   │   ├── components/registry/ # Модульні компоненти реєстру (Table, Toolbar, Modal, Select, DatePicker, Pagination, Toast)
│   │   ├── config/              # Low-Code конфіги реєстрів (tasksRegistry.ts, navigation.json)
│   │   ├── constants/           # Класифікатори (статуси, пріоритети, іконки, кольори)
│   │   ├── layouts/             # CrmLayout.vue (бічне меню, шапка, профіль користувача)
│   │   ├── stores/              # Pinia сховища (auth.ts)
│   │   ├── types/               # TypeScript моделі та конфігураційні інтерфейси
│   │   └── views/               # Сторінки: LoginView, AboutView, RegistryView
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── Dockerfile
├── docker-compose.yml           # Оркестрація PostgreSQL, Redis, Backend, Frontend
└── README.md
```

---

## 🛠 Інструкція з локального запуску

### 1. Передумови
* Встановлений [Docker Desktop](https://www.docker.com/products/docker-desktop/) (або Docker Engine + docker-compose).
* Встановлений `git`.

### 2. Клонування репозиторію
```bash
git clone https://github.com/FarizovM/diia_test_task.git
cd diia_test_task
```

### 3. Запуск контейнерів
Зберіть та запустіть усі сервіси (`task_manager_db`, `task_manager_redis`, `task_manager_backend`, `task_manager_frontend`) у фоновому режимі:

```bash
docker-compose up --build -d
```

Зачекайте кілька секунд, доки база даних PostgreSQL завершить ініціалізацію.

### 4. Застосування міграцій бази даних
Створіть схему таблиць у PostgreSQL через Alembic всередині контейнера бекенду:

```bash
docker exec -it task_manager_backend alembic upgrade head
```

### 5. Генерація тестових даних (Seeding)
Запустіть скрипт, який створить тестового адміністратора та 20 задач із різними пріоритетами, статусами та дедлайнами:

```bash
docker exec -it task_manager_backend python seed.py
```

---

## 🌐 Доступ до сервісів

Після запуску сервіси доступні за адресами:

* **Frontend (Веб-інтерфейс):** [http://localhost:3000](http://localhost:3000)
  * `/login` — Вхід та реєстрація
  * `/about` — Панель моніторингу та аналітики
  * `/registry/tasks` — Реєстр задач (Low-Code таблиця, фільтри, CRUD)
* **Backend API (Swagger UI / OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **OpenAPI Schema (JSON):** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

---

## 🔐 Тестові дані для входу

Для швидкого тестування використовуйте згенерований обліковий запис або зареєструйте нового користувача через форму:

* **Email:** `test@diia.gov.ua`
* **Пароль:** `password123`

---

## 🛑 Корисні команди для розробки

Перегляд логів бекенду:
```bash
docker-compose logs -f backend
```

Перегляд логів фронтенду:
```bash
docker-compose logs -f frontend
```

Перевірка компіляції фронтенду (TypeScript + Vite):
```bash
cd frontend && npm run build
```

Зупинка всіх контейнерів:
```bash
docker-compose down
```

Повна зупинка з видаленням томів бази даних та Redis:
```bash
docker-compose down -v
```
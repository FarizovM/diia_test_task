import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.routes import auth, tasks, users, stats
from app.core.logger import logger

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Операції автентифікації та безпеки: реєстрація нових користувачів, вхід через OAuth2 Password flow, видача JWT-токенів та вихід із занесенням токена до чорного списку Redis.",
    },
    {
        "name": "Tasks",
        "description": "Управління задачами та робота з реєстром: створення, пошук, фільтрація за статусом/пріоритетом/дедлайном, пагінація, редагування та видалення задач.",
    },
    {
        "name": "Users",
        "description": "Керування профілями користувачів та отримання інформації про поточного авторизованого користувача.",
    },
    {
        "name": "Stats",
        "description": "Аналітичні показники та зведена статистика за всіма задачами системи або персональними задачами користувача.",
    },
    {
        "name": "Health",
        "description": "Перевірка працездатності сервісу та доступності бекенду.",
    },
]

app = FastAPI(
    title=f"{settings.PROJECT_NAME} — Сервіс управління задачами",
    description="""
### REST API сервісу управління задачами (Task Manager)

Цей бекенд надає повний набір ендпоінтів для системи управління задачами:
* **Автентифікація:** Реєстрація, OAuth2 Password Bearer токени, безпечний вихід із занесенням токена у чорний список Redis (Blacklist).
* **Реєстр задач:** Повнотекстовий пошук, фільтрація за статусами, пріоритетами, дедлайнами, сортування та серверна пагінація.
* **Статистика:** Агреговані аналітичні показники для дашборду моніторингу.

Всі захищені ендпоінти вимагають передачі заголовка:
`Authorization: Bearer <access_token>`
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        
        log_msg = (
            f"{client_ip} - \"{request.method} {request.url.path}\" "
            f"Status: {response.status_code} - {process_time:.2f}ms"
        )
        
        if response.status_code >= 400:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
            
        return response
    except Exception as exc:
        process_time = (time.perf_counter() - start_time) * 1000
        logger.error(
            f"{client_ip} - \"{request.method} {request.url.path}\" "
            f"FAILED after {process_time:.2f}ms: {exc}",
            exc_info=True,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

@app.get(
    "/health",
    tags=["Health"],
    summary="Перевірка працездатності сервісу",
    description="Повертає поточний статус готовності бекенду для систем моніторингу та балансувальників навантаження.",
    response_description="Статус доступності сервера"
)
async def health_check():
    return {"status": "ok"}
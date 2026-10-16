import urllib.parse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.core.config import settings
from app.core.logger import logger

MUTATING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware для забезпечення безпеки HTTP-заголовків:
    1. Перевірка Origin та Referer для запитів, що модифікують стан (CSRF & Cross-Origin захист).
    2. Додавання захисних HTTP-заголовків у відповіді (X-Frame-Options, X-Content-Type-Options,
       Referrer-Policy, Content-Security-Policy, Permissions-Policy).
    """

    async def dispatch(self, request: Request, call_next):
        # Валідація Origin / Referer для мутуючих методів (POST, PUT, PATCH, DELETE)
        if request.method in MUTATING_METHODS:
            origin = request.headers.get("origin")
            referer = request.headers.get("referer")

            # Перевірка заголовка Origin (якщо запит ініційовано браузером/CORS)
            if origin:
                if origin not in settings.ALLOWED_ORIGINS:
                    logger.warning(
                        f"Заблоковано запит з недійсним Origin: '{origin}' | "
                        f"Метод: {request.method} | Шлях: {request.url.path}"
                    )
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Доступ заборонено: недійсний заголовок Origin"},
                    )

            # Якщо Origin відсутній, але передано Referer
            elif referer:
                parsed_ref = urllib.parse.urlsplit(referer)
                ref_origin = f"{parsed_ref.scheme}://{parsed_ref.netloc}"
                if ref_origin not in settings.ALLOWED_ORIGINS:
                    logger.warning(
                        f"Заблоковано запит з недійсним Referer: '{referer}' (джерело: {ref_origin}) | "
                        f"Метод: {request.method} | Шлях: {request.url.path}"
                    )
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Доступ заборонено: недійсний заголовок Referer"},
                    )

        # Обробка основного запиту
        response: Response = await call_next(request)

        # Встановлення захисних HTTP-заголовків (Security Response Headers)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=(), payment=()"

        # Налаштування Content Security Policy (CSP)
        # Для сторінок інтерактивної документації OpenAPI дозволяємо CDN стилів та скриптів
        if request.url.path in ("/docs", "/redoc", "/api/v1/openapi.json"):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "frame-ancestors 'none';"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "frame-ancestors 'none';"
            )

        return response

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_security_response_headers_present(client: AsyncClient):
    """Перевірка обов'язкових захисних HTTP-заголовків у відповіді"""
    res = await client.get("/health")
    assert res.status_code == 200

    assert res.headers.get("x-frame-options") == "DENY"
    assert res.headers.get("x-content-type-options") == "nosniff"
    assert res.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert res.headers.get("x-xss-protection") == "1; mode=block"
    assert "geolocation=()" in res.headers.get("permissions-policy", "")
    assert "frame-ancestors 'none'" in res.headers.get("content-security-policy", "")

@pytest.mark.asyncio
async def test_docs_content_security_policy(client: AsyncClient):
    """Для сторінок документації CSP дозволяє завантаження CDN ресурсів Swagger"""
    res = await client.get("/docs")
    assert res.status_code == 200
    csp = res.headers.get("content-security-policy", "")
    assert "https://cdn.jsdelivr.net" in csp

@pytest.mark.asyncio
async def test_mutating_request_with_valid_origin(client: AsyncClient, auth_headers: dict):
    """Запит POST з дозволеним Origin успішно виконується"""
    headers = {**auth_headers, "Origin": "http://localhost:3000"}
    res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Тест безпечного Origin", "status": "todo", "priority": "low"},
        headers=headers,
    )
    assert res.status_code == 201

@pytest.mark.asyncio
async def test_mutating_request_with_valid_referer(client: AsyncClient, auth_headers: dict):
    """Запит POST з дозволеним Referer успішно виконується"""
    headers = {**auth_headers, "Referer": "http://localhost:3000/tasks/new"}
    res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Тест безпечного Referer", "status": "todo", "priority": "low"},
        headers=headers,
    )
    assert res.status_code == 201

@pytest.mark.asyncio
async def test_mutating_request_with_forbidden_origin_blocked(client: AsyncClient, auth_headers: dict):
    """Запит POST зі стороннього/фішингового Origin блокується зі статусом 403"""
    headers = {**auth_headers, "Origin": "http://evil-attacker.com"}
    res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Шкідлива задача", "status": "todo", "priority": "high"},
        headers=headers,
    )
    assert res.status_code == 403
    assert "Origin" in res.json().get("detail", "")

@pytest.mark.asyncio
async def test_mutating_request_with_forbidden_referer_blocked(client: AsyncClient, auth_headers: dict):
    """Запит POST зі стороннього Referer (без Origin) блокується зі статусом 403"""
    headers = {**auth_headers, "Referer": "http://evil-attacker.com/malicious-payload"}
    res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Шкідлива задача через Referer", "status": "todo", "priority": "high"},
        headers=headers,
    )
    assert res.status_code == 403
    assert "Referer" in res.json().get("detail", "")

@pytest.mark.asyncio
async def test_safe_get_request_not_blocked_by_referer(client: AsyncClient):
    """Безпечні GET запити не блокуються навіть при наявності зовнішнього Referer"""
    res = await client.get("/health", headers={"Referer": "http://google.com/search"})
    assert res.status_code == 200

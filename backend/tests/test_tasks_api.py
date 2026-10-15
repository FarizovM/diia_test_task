import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_unauthorized_access_blocked(client: AsyncClient):
    """Без токена доступ до реєстру задач має повертати 401"""
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_and_get_task(client: AsyncClient, auth_headers: dict):
    """Створення задачі та перевірка її наявності у списку"""
    payload = {
        "title": "Інтеграція з шлюзом Трембіта",
        "description": "Налаштувати обмін даними",
        "status": "todo",
        "priority": "high"
    }
    create_res = await client.post("/api/v1/tasks/", json=payload, headers=auth_headers)
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "todo"
    task_id = data["task_id"]

    # Отримання списку з фільтром за статусом
    list_res = await client.get("/api/v1/tasks/?status=todo", headers=auth_headers)
    assert list_res.status_code == 200
    registry = list_res.json()
    assert registry["total"] == 1
    assert registry["filtered"] == 1
    tasks = registry["rows"]
    assert len(tasks) == 1
    assert tasks[0]["task_id"] == task_id

@pytest.mark.asyncio
async def test_update_and_delete_task(client: AsyncClient, auth_headers: dict):
    """Редагування статусу задачі та її видалення"""
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Тестова задача", "status": "todo", "priority": "medium"},
        headers=auth_headers,
    )
    task_id = create_res.json()["task_id"]

    # Оновлення статусу на 'done' через PUT
    update_res = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Тестова задача", "status": "done", "priority": "medium"},
        headers=auth_headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "done"

    # Видалення
    del_res = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert del_res.status_code == 204

    # Перевірка, що задачі більше немає в реєстрі
    list_res = await client.get("/api/v1/tasks/", headers=auth_headers)
    assert list_res.status_code == 200
    assert list_res.json()["total"] == 0

@pytest.mark.asyncio
async def test_logout_revokes_token(client: AsyncClient, auth_headers: dict):
    """Після виклику /logout токен потрапляє в Blacklist і більше не працює"""
    logout_res = await client.get("/api/v1/auth/logout", headers=auth_headers)
    assert logout_res.status_code == 200

    # Повторний запит із тим самим токеном має повернути 401
    me_res = await client.get("/api/v1/users/me", headers=auth_headers)
    assert me_res.status_code == 401
import json
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_stats_cached_in_redis_on_request(client: AsyncClient, auth_headers: dict, redis_mock):
    """При запиті до /stats/all та /stats/me дані кешуються в Redis"""
    # Спочатку кеш порожній
    assert await redis_mock.get("stats:all") is None

    res_all = await client.get("/api/v1/stats/all", headers=auth_headers)
    assert res_all.status_code == 200
    data_all = res_all.json()

    # Перевіряємо, що в Redis з'явився ключ stats:all
    cached_all = await redis_mock.get("stats:all")
    assert cached_all is not None
    assert json.loads(cached_all)["total"] == data_all["total"]

    # Робимо запит до персональної статистики
    res_me = await client.get("/api/v1/stats/me", headers=auth_headers)
    assert res_me.status_code == 200

    # Перевіряємо наявність персонального ключа користувача
    keys = list(redis_mock.store.keys())
    user_stat_keys = [k for k in keys if k.startswith("stats:user:")]
    assert len(user_stat_keys) == 1

@pytest.mark.asyncio
async def test_stats_cache_updated_on_task_create(client: AsyncClient, auth_headers: dict, redis_mock):
    """Створення задачі автоматично оновлює кеш статистики в Redis"""
    # Отримуємо початкову статистику
    res = await client.get("/api/v1/stats/all", headers=auth_headers)
    initial_total = res.json()["total"]
    initial_todo = res.json()["todo"]

    # Створюємо нову задачу
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Нова задача для перевірки кешу", "status": "todo", "priority": "high"},
        headers=auth_headers,
    )
    assert create_res.status_code == 201

    # Перевіряємо, що в Redis кеш stats:all вже ОНОВИВСЯ без повторного запиту до /stats/all
    cached_all = await redis_mock.get("stats:all")
    assert cached_all is not None
    cached_data = json.loads(cached_all)
    assert cached_data["total"] == initial_total + 1
    assert cached_data["todo"] == initial_todo + 1
    assert cached_data["high"] >= 1

@pytest.mark.asyncio
async def test_stats_cache_updated_on_task_update(client: AsyncClient, auth_headers: dict, redis_mock):
    """Редагування статусу задачі автоматично оновлює розподіл статусів у кеші Redis"""
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Задача для тесту редагування", "status": "todo", "priority": "medium"},
        headers=auth_headers,
    )
    task_id = create_res.json()["task_id"]

    cached_before = json.loads(await redis_mock.get("stats:all"))
    todo_before = cached_before["todo"]
    done_before = cached_before["done"]

    # Змінюємо статус задачі на 'done'
    update_res = await client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Задача для тесту редагування", "status": "done", "priority": "medium"},
        headers=auth_headers,
    )
    assert update_res.status_code == 200

    # Перевіряємо оновлення в Redis кеші
    cached_after = json.loads(await redis_mock.get("stats:all"))
    assert cached_after["todo"] == todo_before - 1
    assert cached_after["done"] == done_before + 1

@pytest.mark.asyncio
async def test_stats_cache_updated_on_task_delete(client: AsyncClient, auth_headers: dict, redis_mock):
    """Видалення задачі автоматично зменшує лічильники в кеші Redis"""
    create_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Задача під видалення", "status": "todo", "priority": "low"},
        headers=auth_headers,
    )
    task_id = create_res.json()["task_id"]

    cached_before = json.loads(await redis_mock.get("stats:all"))
    total_before = cached_before["total"]

    # Видаляємо задачу
    del_res = await client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert del_res.status_code == 204

    # Перевіряємо, що в Redis загальна кількість зменшилась
    cached_after = json.loads(await redis_mock.get("stats:all"))
    assert cached_after["total"] == total_before - 1

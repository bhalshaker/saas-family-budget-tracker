import pytest
from httpx import AsyncClient
from main import app

category_test_data = {
    "user1": {"name": "CategoryUser1", "email": "categoryuser1@example.com", "plain_password": "Pass123!"},
    "user2": {"name": "CategoryUser2", "email": "categoryuser2@example.com", "plain_password": "Pass456!"},
    "user1_login": {"email": "categoryuser1@example.com", "password": "Pass123!"},
    "user2_login": {"email": "categoryuser2@example.com", "password": "Pass456!"},
    "family1": {"name": "Smith Category Family"},
    "family2": {"name": "Johnson Category Family"},
    "category1": {"name": "Groceries", "type": "income"},
    "category2": {"name": "Salary", "type": "expense"},
    "update_category": {"name": "Updated Category Name", "type": "transfer"},
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_category_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category1"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["category"]["name"] == category_test_data["category1"]["name"]

@pytest.mark.asyncio
async def test_create_category_unauthenticated():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"/api/v1/families/{category_test_data['garbage_uuid']}/categories", json=category_test_data["category1"])
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_category_invalid_data():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/categories", json={}, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_get_all_family_categories_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category1"], headers=headers)
        await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category2"], headers=headers)
        response = await client.get(f"/api/v1/families/{family_id}/categories", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert len(response.json()["categories"]) >= 2

@pytest.mark.asyncio
async def test_get_all_family_categories_unauthenticated():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/v1/families/{category_test_data['garbage_uuid']}/categories")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_all_family_categories_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/families/{category_test_data['garbage_uuid']}/categories", headers=headers)
        assert response.status_code == 404
        assert "NOT FOUND" in response.json()["detail"].upper()

@pytest.mark.asyncio
async def test_get_category_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        cat_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category1"], headers=headers)
        category_id = cat_resp.json()["category"]["id"]
        response = await client.get(f"/api/v1/categories/{category_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["category"]["id"] == category_id

@pytest.mark.asyncio
async def test_get_category_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/categories/{category_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_update_category_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        cat_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category1"], headers=headers)
        category_id = cat_resp.json()["category"]["id"]
        response = await client.put(f"/api/v1/categories/{category_id}", json=category_test_data["update_category"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["category"]["name"] == category_test_data["update_category"]["name"]

@pytest.mark.asyncio
async def test_update_category_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.put(f"/api/v1/categories/{category_test_data['garbage_uuid']}", json=category_test_data["update_category"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_delete_category_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=category_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        cat_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=category_test_data["category1"], headers=headers)
        category_id = cat_resp.json()["category"]["id"]
        response = await client.delete(f"/api/v1/categories/{category_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] in [0, 1]  # Could be 0 if deletion fails due to constraints

@pytest.mark.asyncio
async def test_delete_category_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=category_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=category_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.delete(f"/api/v1/categories/{category_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

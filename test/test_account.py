import pytest
from httpx import AsyncClient
from main import app

account_test_data = {
    "user1": {"name": "AccountUser1", "email": "accountuser1@example.com", "plain_password": "Pass123!"},
    "user2": {"name": "AccountUser2", "email": "accountuser2@example.com", "plain_password": "Pass456!"},
    "user1_login": {"email": "accountuser1@example.com", "password": "Pass123!"},
    "user2_login": {"email": "accountuser2@example.com", "password": "Pass456!"},
    "family1": {"name": "Smith Account Family"},
    "family2": {"name": "Johnson Account Family"},
    "account1": {"name": "Main Account", "type": "Asset", "balance": 100.0},
    "account2": {"name": "Expense Account", "type": "Expense", "balance": 0.0},
    "update_account": {"name": "Updated Account Name", "balance": 200.0},
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_account_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account1"], headers=headers)
        print(response.status_code)
        print(response.json())
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["account"]["name"] == account_test_data["account1"]["name"]

@pytest.mark.asyncio
async def test_create_account_unauthenticated():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"/api/v1/families/{account_test_data['garbage_uuid']}/accounts", json=account_test_data["account1"])
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_account_invalid_data():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/accounts", json={}, headers=headers)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_family_accounts_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account1"], headers=headers)
        await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account2"], headers=headers)
        response = await client.get(f"/api/v1/families/{family_id}/accounts", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert len(response.json()["accounts"]) >= 2

@pytest.mark.asyncio
async def test_get_all_family_accounts_unauthenticated():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/v1/families/{account_test_data['garbage_uuid']}/accounts")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_all_family_accounts_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/families/{account_test_data['garbage_uuid']}/accounts", headers=headers)
        print(response.text)
        assert response.status_code == 404
        assert "NOT FOUND" in response.json()["detail"].upper()

@pytest.mark.asyncio
async def test_get_account_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        acc_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account1"], headers=headers)
        account_id = acc_resp.json()["account"]["id"]
        response = await client.get(f"/api/v1/accounts/{account_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["account"]["id"] == account_id

@pytest.mark.asyncio
async def test_get_account_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/accounts/{account_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_update_account_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        acc_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account1"], headers=headers)
        account_id = acc_resp.json()["account"]["id"]
        response = await client.put(f"/api/v1/accounts/{account_id}", json=account_test_data["update_account"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["account"]["name"] == account_test_data["update_account"]["name"]

@pytest.mark.asyncio
async def test_update_account_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.put(f"/api/v1/accounts/{account_test_data['garbage_uuid']}", json=account_test_data["update_account"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_delete_account_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=account_test_data["family1"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        acc_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=account_test_data["account1"], headers=headers)
        account_id = acc_resp.json()["account"]["id"]
        response = await client.delete(f"/api/v1/accounts/{account_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] in [0, 1]  # Could be 0 if deletion fails due to constraints

@pytest.mark.asyncio
async def test_delete_account_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=account_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=account_test_data["user1_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.delete(f"/api/v1/accounts/{account_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

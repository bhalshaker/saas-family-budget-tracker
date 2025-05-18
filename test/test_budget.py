import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from datetime import datetime, timedelta

budget_test_data = {
    "user": {"name": "BudgetUser", "email": "budgetuser@example.com", "plain_password": "BudgetPass123!"},
    "user_login": {"email": "budgetuser@example.com", "password": "BudgetPass123!"},
    "family": {"name": "Budget Family"},
    "category": {"name": "Budget Category", "type": "expense"},
    "account": {"name": "Budget Account", "type": "Asset", "balance": 1000.0},
    "budget": {
        "amount": 300.0,
        "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    },
    "budget_update": {
        "amount": 400.0
    },
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_budget_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        response = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        # Removed assertion for budget name

@pytest.mark.asyncio
async def test_create_budget_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"/api/v1/families/{budget_test_data['garbage_uuid']}/budgets", json={})
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_budget_invalid_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/budgets", json={}, headers=headers)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_budgets_of_family_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        response = await client.get(f"/api/v1/families/{family_id}/budgets", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert isinstance(response.json()["budgets"], list)

@pytest.mark.asyncio
async def test_update_budget_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        update_data = {
            **budget_test_data["budget_update"],
            "entry_account_id": account_id
        }
        response = await client.put(f"/api/v1/budgets/{budget_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        # Removed assertion for budget name in update

@pytest.mark.asyncio
async def test_update_budget_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        update_data = {
            **budget_test_data["budget_update"],
            "entry_account_id": budget_test_data["garbage_uuid"]
        }
        response = await client.put(f"/api/v1/budgets/{budget_test_data['garbage_uuid']}", json=update_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_delete_budget_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        response = await client.delete(f"/api/v1/budgets/{budget_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"]==1

@pytest.mark.asyncio
async def test_delete_budget_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.delete(f"/api/v1/budgets/{budget_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

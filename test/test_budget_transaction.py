import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from datetime import datetime, timedelta

budget_transaction_test_data = {
    "user": {"name": "BudgetTransUser", "email": "budgettransuser@example.com", "plain_password": "BudgetTransPass123!"},
    "user_login": {"email": "budgettransuser@example.com", "password": "BudgetTransPass123!"},
    "family": {"name": "BudgetTrans Family"},
    "category": {"name": "BudgetTrans Category", "type": "expense"},
    "account": {"name": "BudgetTrans Account", "type": "Asset", "balance": 1000.0},
    "budget": {
        "amount": 500.0,
        "start_date": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    },
    "transaction": {
        "amount": 100.0,
        "description": "Budget transaction test",
        "transaction_type": "expense"
    },
    "budget_transaction": {
        "assigned_amount": 80.0
    },
    "budget_transaction_update": {
        "assigned_amount": 120.0
    },
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_budget_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_transaction_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": budget_transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": budget_transaction_test_data["transaction"]["description"],
            "transaction_type": budget_transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        budget_transaction_data = {
            "entry_budget_id": budget_id,
            "entry_transaction_id": transaction_id,
            "assigned_amount": budget_transaction_test_data["budget_transaction"]["assigned_amount"]
        }
        response = await client.post(f"/api/v1/families/{family_id}/budget_transactions", json=budget_transaction_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["budget_transaction"]["assigned_amount"] == float(budget_transaction_data["assigned_amount"])

@pytest.mark.asyncio
async def test_create_budget_transaction_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"/api/v1/families/{budget_transaction_test_data['garbage_uuid']}/budget_transactions", json={})
        assert response.status_code in [401, 403]

@pytest.mark.asyncio
async def test_create_budget_transaction_invalid_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/budget_transactions", json={}, headers=headers)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_budget_transactions_of_family_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_transaction_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": budget_transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": budget_transaction_test_data["transaction"]["description"],
            "transaction_type": budget_transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        budget_transaction_data = {
            "entry_budget_id": budget_id,
            "entry_transaction_id": transaction_id,
            "assigned_amount": budget_transaction_test_data["budget_transaction"]["assigned_amount"]
        }
        await client.post(f"/api/v1/families/{family_id}/budget_transactions", json=budget_transaction_data, headers=headers)
        response = await client.get(f"/api/v1/families/{family_id}/budget_transactions", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert isinstance(response.json()["budget_transactions"], list)

@pytest.mark.asyncio
async def test_get_budget_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_transaction_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": budget_transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": budget_transaction_test_data["transaction"]["description"],
            "transaction_type": budget_transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        budget_transaction_data = {
            "entry_budget_id": budget_id,
            "entry_transaction_id": transaction_id,
            "assigned_amount": budget_transaction_test_data["budget_transaction"]["assigned_amount"]
        }
        budget_trans_resp = await client.post(f"/api/v1/families/{family_id}/budget_transactions", json=budget_transaction_data, headers=headers)
        budget_transaction_id = budget_trans_resp.json()["budget_transaction"]["id"]
        response = await client.get(f"/api/v1/budget_transactions/{budget_transaction_id}", headers=headers)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["budget_transaction"]["id"] == budget_transaction_id

@pytest.mark.asyncio
async def test_get_budget_transaction_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/budget_transactions/{budget_transaction_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_delete_budget_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=budget_transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=budget_transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=budget_transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        budget_data = {
            **budget_transaction_test_data["budget"],
            "entry_category_id": category_id,
            "entry_account_id": account_id
        }
        budget_resp = await client.post(f"/api/v1/families/{family_id}/budgets", json=budget_data, headers=headers)
        budget_id = budget_resp.json()["budget"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": budget_transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": budget_transaction_test_data["transaction"]["description"],
            "transaction_type": budget_transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        budget_transaction_data = {
            "entry_budget_id": budget_id,
            "entry_transaction_id": transaction_id,
            "assigned_amount": budget_transaction_test_data["budget_transaction"]["assigned_amount"]
        }
        budget_trans_resp = await client.post(f"/api/v1/families/{family_id}/budget_transactions", json=budget_transaction_data, headers=headers)
        budget_transaction_id = budget_trans_resp.json()["budget_transaction"]["id"]
        response = await client.delete(f"/api/v1/budget_transactions/{budget_transaction_id}", headers=headers)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["code"] == 1

@pytest.mark.asyncio
async def test_delete_budget_transaction_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=budget_transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=budget_transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.delete(f"/api/v1/budget_transactions/{budget_transaction_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")
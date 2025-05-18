import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from uuid import uuid4
from datetime import datetime

transaction_test_data = {
    "user": {"name": "TransUser", "email": "transuser@example.com", "plain_password": "TransPass123!"},
    "user_login": {"email": "transuser@example.com", "password": "TransPass123!"},
    "family": {"name": "Transaction Family"},
    "category": {"name": "Groceries", "type": "expense"},
    "account": {"name": "Wallet", "type": "Asset", "balance": 500.0},
    "transaction": {
        "amount": 100.0,
        "description": "Grocery shopping",
        "transaction_type": "expense"
    },
    "transaction_update": {
        "amount": 150.0,
        "description": "Updated groceries"
    },
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Create user and login
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        # Create family
        family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        # Create category
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        # Create account
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        # Create transaction
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": transaction_test_data["transaction"]["description"],
            "transaction_type": transaction_test_data["transaction"]["transaction_type"]
        }
        response = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["transaction"]["amount"] == transaction_data["amount"]

@pytest.mark.asyncio
async def test_create_transaction_unauthenticated():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(f"/api/v1/families/{transaction_test_data['garbage_uuid']}/transactions", json={})
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_transaction_invalid_data():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        response = await client.post(f"/api/v1/families/{family_id}/transactions", json={}, headers=headers)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_transactions_of_family_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": transaction_test_data["transaction"]["description"],
            "transaction_type": transaction_test_data["transaction"]["transaction_type"]
        }
        await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        response = await client.get(f"/api/v1/families/{family_id}/transactions", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert isinstance(response.json()["transactions"], list)

@pytest.mark.asyncio
async def test_get_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": transaction_test_data["transaction"]["description"],
            "transaction_type": transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        response = await client.get(f"/api/v1/transactions/{transaction_id}", headers=headers)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["transaction"]["id"] == transaction_id

@pytest.mark.asyncio
async def test_get_transaction_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/transactions/{transaction_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_update_transaction_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=transaction_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=transaction_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=transaction_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": transaction_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": transaction_test_data["transaction"]["description"],
            "transaction_type": transaction_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        response = await client.put(f"/api/v1/transactions/{transaction_id}", json=transaction_test_data["transaction_update"], headers=headers)
        print(response.text)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert response.json()["transaction"]["amount"] == transaction_test_data["transaction_update"]["amount"]

# @pytest.mark.asyncio
# async def test_update_transaction_not_found():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         await client.post("/api/v1/users/", json=transaction_test_data["user"])
#         login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
#         token = login_resp.json().get("user_key", {}).get("authorization")
#         headers = {"Authorization": token} if token else {}
#         response = await client.put(f"/api/v1/transactions/{transaction_test_data['garbage_uuid']}", json=transaction_test_data["transaction_update"], headers=headers)
#         assert response.status_code == 200
#         assert response.json()["code"] == 0
#         assert response.json()["status"].upper().startswith("FAILED")

# @pytest.mark.asyncio
# async def test_delete_transaction_success():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         await client.post("/api/v1/users/", json=transaction_test_data["user"])
#         login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
#         token = login_resp.json().get("user_key", {}).get("authorization")
#         headers = {"Authorization": token} if token else {}
#         family_resp = await client.post("/api/v1/families/", json=transaction_test_data["family"], headers=headers)
#         family_id = family_resp.json()["family"]["id"]
#         category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=transaction_test_data["category"], headers=headers)
#         category_id = category_resp.json()["category"]["id"]
#         account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=transaction_test_data["account"], headers=headers)
#         account_id = account_resp.json()["account"]["id"]
#         transaction_data = {
#             "category_id": category_id,
#             "account_id": account_id,
#             "amount": transaction_test_data["transaction"]["amount"],
#             "date": datetime.utcnow().isoformat(),
#             "description": transaction_test_data["transaction"]["description"],
#             "type": transaction_test_data["transaction"]["type"]
#         }
#         trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
#         transaction_id = trans_resp.json()["transaction"]["id"]
#         response = await client.delete(f"/api/v1/transactions/{transaction_id}", headers=headers)
#         assert response.status_code == 200
#         assert response.json()["code"] in [0, 1]

# @pytest.mark.asyncio
# async def test_delete_transaction_not_found():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as client:
#         await client.post("/api/v1/users/", json=transaction_test_data["user"])
#         login_resp = await client.post("/api/v1/users/login", json=transaction_test_data["user_login"])
#         token = login_resp.json().get("user_key", {}).get("authorization")
#         headers = {"Authorization": token} if token else {}
#         response = await client.delete(f"/api/v1/transactions/{transaction_test_data['garbage_uuid']}", headers=headers)
#         assert response.status_code == 200
#         assert response.json()["code"] == 0
#         assert response.json()["status"].upper().startswith("FAILED")

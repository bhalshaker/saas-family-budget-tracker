import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from pathlib import Path
from datetime import datetime

attachment_test_data = {
    "user": {"name": "AttachmentUser", "email": "attachmentuser@example.com", "plain_password": "AttachPass123!"},
    "user_login": {"email": "attachmentuser@example.com", "password": "AttachPass123!"},
    "family": {"name": "Attachment Family"},
    "category": {"name": "Attachment Category", "type": "expense"},
    "account": {"name": "Attachment Account", "type": "Asset", "balance": 1000.0},
    "transaction": {
        "amount": 50.0,
        "description": "Attachment test transaction",
        "transaction_type": "expense"
    },
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

def get_test_file(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test attachment file.")
    return test_file

@pytest.mark.asyncio
async def test_upload_attachment_success(tmp_path):
    test_file = get_test_file(tmp_path)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=attachment_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=attachment_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        family_resp = await client.post("/api/v1/families/", json=attachment_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        category_resp = await client.post(f"/api/v1/families/{family_id}/categories", json=attachment_test_data["category"], headers=headers)
        category_id = category_resp.json()["category"]["id"]
        account_resp = await client.post(f"/api/v1/families/{family_id}/accounts", json=attachment_test_data["account"], headers=headers)
        account_id = account_resp.json()["account"]["id"]
        transaction_data = {
            "category_id": category_id,
            "account_id": account_id,
            "amount": attachment_test_data["transaction"]["amount"],
            "date": datetime.utcnow().isoformat(),
            "description": attachment_test_data["transaction"]["description"],
            "transaction_type": attachment_test_data["transaction"]["transaction_type"]
        }
        trans_resp = await client.post(f"/api/v1/families/{family_id}/transactions", json=transaction_data, headers=headers)
        transaction_id = trans_resp.json()["transaction"]["id"]
        with open(test_file, "rb") as f:
            files = {"file": ("test_file.txt", f, "text/plain")}
            response = await client.post(f"/api/v1/transactions/{transaction_id}/attachments", files=files, headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert "attachment" in response.json()
        attachment_id = response.json()["attachment"]["id"]
        return attachment_id, transaction_id, headers

@pytest.mark.asyncio
async def test_upload_attachment_unauthenticated(tmp_path):
    test_file = get_test_file(tmp_path)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        files = {"file": ("test_file.txt", open(test_file, "rb"), "text/plain")}
        response = await client.post(f"/api/v1/transactions/{attachment_test_data['garbage_uuid']}/attachments", files=files)
        assert response.status_code in [401, 403]

@pytest.mark.asyncio
async def test_get_attachment_of_transaction_success(tmp_path):
    attachment_id, transaction_id, headers = await test_upload_attachment_success(tmp_path)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/v1/transactions/{transaction_id}/attachments", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 1
        assert response.json()["status"].upper().startswith("SUCCESS")
        assert "attachment" in response.json()

@pytest.mark.asyncio
async def test_get_attachment_of_transaction_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=attachment_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=attachment_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.get(f"/api/v1/transactions/{attachment_test_data['garbage_uuid']}/attachments", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

@pytest.mark.asyncio
async def test_retrieve_attachment_success(tmp_path):
    attachment_id, transaction_id, headers = await test_upload_attachment_success(tmp_path)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/v1/attachments/{attachment_id}", headers=headers)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/octet-stream")

@pytest.mark.asyncio
async def test_delete_attachment_success(tmp_path):
    attachment_id, transaction_id, headers = await test_upload_attachment_success(tmp_path)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(f"/api/v1/attachments/{attachment_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"]==1

@pytest.mark.asyncio
async def test_delete_attachment_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=attachment_test_data["user"])
        login_resp = await client.post("/api/v1/users/login", json=attachment_test_data["user_login"])
        token = login_resp.json().get("user_key", {}).get("authorization")
        headers = {"Authorization": token} if token else {}
        response = await client.delete(f"/api/v1/attachments/{attachment_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].upper().startswith("FAILED")

# filepath: /home/proj/vscode/saas-family-budget-tracker/test/test_familyuser.py
import pytest
from httpx import AsyncClient
from main import app

family_user_test_data = {
    "owner": {"name": "OwnerUser", "email": "owneruser@example.com", "plain_password": "OwnerPass123!"},
    "member": {"name": "MemberUser", "email": "memberuser@example.com", "plain_password": "MemberPass123!"},
    "guest": {"name": "GuestUser", "email": "guestuser@example.com", "plain_password": "GuestPass123!"},
    "owner_login": {"email": "owneruser@example.com", "password": "OwnerPass123!"},
    "member_login": {"email": "memberuser@example.com", "password": "MemberPass123!"},
    "guest_login": {"email": "guestuser@example.com", "password": "GuestPass123!"},
    "family": {"name": "Test Family"},
    "family2": {"name": "Second Test Family"},
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_get_all_users_in_family_success():
    """Test getting all users in a family as a member."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register owner and member
        owner_response=await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        owner_id = owner_response.json()["user"]["id"]
        memeber_response=await client.post("/api/v1/users/", json=family_user_test_data["member"])
        member_id = memeber_response.json()["user"]["id"]
        #Login as owner
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        # Create family as owner
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        # Add member to family
        add_member_payload = {"user_id": member_id, "user_role": "child"}
        add_member_resp=await client.post(f"/api/v1/families/{family_id}/users", json=add_member_payload, headers=headers)
        print("Add member response:", add_member_resp.json())  # Debug print
        assert add_member_resp.status_code == 200
        assert add_member_resp.json()["code"] == 1
        # Get all users in family as owner
        resp = await client.get(f"/api/v1/families/{family_id}/users", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 1
        assert "users" in resp.json()
        assert owner_id in resp.json()["users"]
        assert member_id in resp.json()["users"]

@pytest.mark.asyncio
async def test_get_all_users_in_family_unauthorized():
    """Test getting all users in a family as a non-member (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        await client.post("/api/v1/users/", json=family_user_test_data["guest"])
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        # Login as guest (not a member)
        guest_login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["guest_login"])
        guest_token = guest_login_resp.json()["user_key"]["authorization"]
        guest_headers = {"Authorization": guest_token}
        resp = await client.get(f"/api/v1/families/{family_id}/users", headers=guest_headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert resp.json()["status"].upper() == "UNAUTHORIZED"

@pytest.mark.asyncio
async def test_get_all_users_in_family_not_found():
    """Test getting users for a non-existent family."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        resp = await client.get(f"/api/v1/families/{family_user_test_data['garbage_uuid']}/users", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert resp.json()["status"].upper() == "FAILED"

@pytest.mark.asyncio
async def test_add_user_to_family_success():
    """Test adding a user to a family as owner."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        member_resp=await client.post("/api/v1/users/", json=family_user_test_data["member"])
        member_id = member_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        add_member_payload = {"user_id": member_id, "user_role": "child"}
        resp = await client.post(f"/api/v1/families/{family_id}/users", json=add_member_payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 1
        assert resp.json()["status"].upper() == "SUCCESS"

@pytest.mark.asyncio
async def test_add_user_to_family_already_member():
    """Test adding a user who is already a member (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        owner_resp=await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        owner_id = owner_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        add_member_payload = {"user_id": owner_id, "user_role": "child"}
        resp = await client.post(f"/api/v1/families/{family_id}/users", json=add_member_payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert "already" in resp.json()["message"].lower()

@pytest.mark.asyncio
async def test_add_user_to_family_not_found():
    """Test adding a user to a non-existent family (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        member_resp=await client.post("/api/v1/users/", json=family_user_test_data["member"])
        member_id = member_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        add_member_payload = {"user_id": member_id, "user_role": "child"}
        resp = await client.post(f"/api/v1/families/{family_user_test_data['garbage_uuid']}/users", json=add_member_payload, headers=headers)
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()

@pytest.mark.asyncio
async def test_add_user_to_family_user_not_found():
    """Test adding a non-existent user to a family (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        add_member_payload = {"user_id": family_user_test_data["garbage_uuid"], "user_role": "child"}
        resp = await client.post(f"/api/v1/families/{family_id}/users", json=add_member_payload, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert "not found" in resp.json()["message"].lower()

@pytest.mark.asyncio
async def test_remove_user_from_family_success():
    """Test removing a user from a family as owner."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        member_resp=await client.post("/api/v1/users/", json=family_user_test_data["member"])
        member_id = member_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        add_member_payload = {"user_id": member_id, "user_role": "child"}
        await client.post(f"/api/v1/families/{family_id}/users", json=add_member_payload, headers=headers)
        resp = await client.delete(f"/api/v1/families/{family_id}/users/{member_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 1
        assert "removed" in resp.json()["message"].lower()

@pytest.mark.asyncio
async def test_remove_user_from_family_not_found():
    """Test removing a user not in the family (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        resp = await client.delete(f"/api/v1/families/{family_id}/users/{family_user_test_data['garbage_uuid']}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert "not found" in resp.json()["message"].lower()

@pytest.mark.asyncio
async def test_remove_user_from_family_cannot_remove_owner():
    """Test removing the owner from the family (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        owner_resp=await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        owner_id = owner_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        family_resp = await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        family_id = family_resp.json()["family"]["id"]
        resp = await client.delete(f"/api/v1/families/{family_id}/users/{owner_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert "owner" in resp.json()["message"].lower()

@pytest.mark.asyncio
async def test_get_families_user_belongs_to_success():
    """Test getting all families a user belongs to (self)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        user_resp=  await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        user_id = user_resp.json()["user"]["id"]
        login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        token = login_resp.json()["user_key"]["authorization"]
        headers = {"Authorization": token}
        await client.post("/api/v1/families/", json=family_user_test_data["family"], headers=headers)
        await client.post("/api/v1/families/", json=family_user_test_data["family2"], headers=headers)
        resp = await client.get(f"/api/v1/users/{user_id}/families", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 1
        print("Response:", resp.json())  # Debug print

@pytest.mark.asyncio
async def test_get_families_user_belongs_to_unauthorized():
    """Test getting families for another user (should fail)."""
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_user_test_data["owner"])
        member_resp=await client.post("/api/v1/users/", json=family_user_test_data["member"])
        member_id = member_resp.json()["user"]["id"]
        owner_login_resp = await client.post("/api/v1/users/login", json=family_user_test_data["owner_login"])
        owner_token = owner_login_resp.json()["user_key"]["authorization"]
        owner_headers = {"Authorization": owner_token}
        # Owner tries to get member's families
        resp = await client.get(f"/api/v1/users/{member_id}/families", headers=owner_headers)
        assert resp.status_code == 200
        assert resp.json()["code"] == 0
        assert "not authorized" in resp.json()["message"].lower()

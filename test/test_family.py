import pytest
from httpx import AsyncClient
from main import app

family_test_data = {
    "user1": {"name": "FamilyUser1", "email": "familyuser1@example.com", "plain_password": "Pass123!"},
    "user2": {"name": "FamilyUser2", "email": "familyuser2@example.com", "plain_password": "Pass456!"},
    "user1_login": {"email": "familyuser1@example.com", "password": "Pass123!"},
    "user2_login": {"email": "familyuser2@example.com", "password": "Pass456!"},
    "family1": {"name": "Smith Family"},
    "family2": {"name": "Johnson Family"},
    "update_family": {"name": "Updated Family Name"},
    "garbage_uuid": "00000000-0000-0000-0000-000000000000"
}

@pytest.mark.asyncio
async def test_create_family_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        response = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        print("Family creation response:", response.text)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        assert response.json()["code"] == 1
        assert response.json()["status"] == "SUCCESSFUL"
        assert response.json()["family"]["name"] == family_test_data["family1"]["name"]

@pytest.mark.asyncio
async def test_create_family_unauthenticated():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/families/", json=family_test_data["family1"])
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_family_invalid_data():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        response = await client.post("/api/v1/families/", json={}, headers=headers)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_all_families():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create two families
        await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        await client.post("/api/v1/families/", json=family_test_data["family2"], headers=headers)
        #Get all families
        response = await client.get("/api/v1/families/", headers=headers)
        assert response.status_code == 200
        assert "families" in response.json()
        assert len(response.json()["families"]) > 0

@pytest.mark.asyncio
async def test_get_family_by_id():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create a family
        create_resp = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        family_id = create_resp.json()["family"]["id"]
        #Get the family by ID
        response = await client.get(f"/api/v1/families/{family_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["family"]["id"] == family_id

@pytest.mark.asyncio
async def test_get_family_by_id_unauthorized():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        #Create a user
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        #Login as the user
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        #Create the family authonticated
        family_response = await client.post("/api/v1/families/", json=family_test_data["family1"], headers={"Authorization": login_json["user_key"]["authorization"]})
        family_id = family_response.json()["family"]["id"]
        #Get the family by ID without authentication
        response = await client.get(f"/api/v1/families/{family_id}")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_family_by_id_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Try to get a family that does not exist
        response = await client.get(f"/api/v1/families/{family_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].lower() == "failed"
        assert "not found" in response.json()["message"].lower()


@pytest.mark.asyncio
async def test_update_family_success():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create a family
        create_resp = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        family_id = create_resp.json()["family"]["id"]
        #Update the family
        response = await client.put(f"/api/v1/families/{family_id}", json=family_test_data["update_family"], headers=headers)
        assert response.status_code == 200
        print("Update family response:", response.text)
        assert response.json()["code"] == 1
        assert response.json()["status"] == "SUCCESSFUL"
        assert response.json()["family"]["name"] == family_test_data["update_family"]["name"]
    
@pytest.mark.asyncio
async def test_update_family_unauthorized():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        #Create a user
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        #Login as the user
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create a family
        create_resp = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        family_id = create_resp.json()["family"]["id"]
        #Update the family without authentication
        response = await client.put(f"/api/v1/families/{family_id}", json=family_test_data["update_family"])
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_family_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Update a family that does not exist
        response = await client.put(f"/api/v1/families/{family_test_data['garbage_uuid']}", json=family_test_data["update_family"], headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].lower() == "failed"
        assert "not found" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_delete_family_success_fail():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create a family
        create_resp = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        family_id = create_resp.json()["family"]["id"]
        #Delete the family
        response = await client.delete(f"/api/v1/families/{family_id}", headers=headers)
        assert response.status_code == 200
        #Record can not be deleted unless famlily_users record is deleted and this will be covered in family_users test

@pytest.mark.asyncio
async def test_delete_family_unauthorized():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        #Create a user
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        #Login as the user
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Create a family
        create_resp = await client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
        family_id = create_resp.json()["family"]["id"]
        #Delete the family without authentication
        response = await client.delete(f"/api/v1/families/{family_id}")
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_delete_family_not_found():
    from httpx import ASGITransport, AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/users/", json=family_test_data["user1"])
        login_resp = await client.post("/api/v1/users/login", json=family_test_data["user1_login"])
        try:
            login_json = login_resp.json()
        except Exception:
            print("Login response text:", login_resp.text)
            assert False, "Login did not return valid JSON"
        assert login_json is not None, f"Login response JSON is None. Status: {login_resp.status_code}, Text: {login_resp.text}"
        token = login_json.get("user_key", {}).get("authorization") if login_json.get("user_key") else None
        headers = {"Authorization": token} if token else {}
        #Delete a family that does not exist
        response = await client.delete(f"/api/v1/families/{family_test_data['garbage_uuid']}", headers=headers)
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["status"].lower() == "failed"
        assert "not found" in response.json()["message"].lower()
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

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

def create_and_login_user(user_data, login_data):
    client.post("/api/v1/users/", json=user_data)
    login_resp = client.post("/api/v1/users/login", json=login_data)
    token = login_resp.json().get("user_key", {}).get("authorization")
    return {"Authorization": token} if token else {}

def test_create_family_success():
    headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
    response = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"] == "SUCCESSFUL"
    assert response.json()["family"]["name"] == family_test_data["family1"]["name"]

# def test_create_family_unauthenticated():
#     response = client.post("/api/v1/families/", json=family_test_data["family2"])
#     assert response.status_code in [401, 403]

# def test_get_all_families():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
#     response = client.get("/api/v1/families/")
#     assert response.status_code == 200
#     assert "families" in response.json()

# def test_get_family_by_id_success():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
#     family_id = create_resp.json()["family"]["id"]
#     response = client.get(f"/api/v1/families/{family_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 1
#     assert response.json()["family"]["id"] == family_id

# def test_get_family_by_id_unauthorized():
#     headers1 = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers1)
#     family_id = create_resp.json()["family"]["id"]
#     headers2 = create_and_login_user(family_test_data["user2"], family_test_data["user2_login"])
#     response = client.get(f"/api/v1/families/{family_id}", headers=headers2)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "forbidden" in response.json()["message"].lower() or "not allowed" in response.json()["message"].lower()

# def test_get_family_by_id_not_found():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     response = client.get(f"/api/v1/families/{family_test_data['garbage_uuid']}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "not found" in response.json()["message"].lower()

# def test_update_family_success():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
#     family_id = create_resp.json()["family"]["id"]
#     response = client.put(f"/api/v1/families/{family_id}", json=family_test_data["update_family"], headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 1
#     assert response.json()["family"]["name"] == family_test_data["update_family"]["name"]

# def test_update_family_unauthorized():
#     headers1 = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers1)
#     family_id = create_resp.json()["family"]["id"]
#     headers2 = create_and_login_user(family_test_data["user2"], family_test_data["user2_login"])
#     response = client.put(f"/api/v1/families/{family_id}", json=family_test_data["update_family"], headers=headers2)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "forbidden" in response.json()["message"].lower() or "not allowed" in response.json()["message"].lower()

# def test_update_family_not_found():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     response = client.put(f"/api/v1/families/{family_test_data['garbage_uuid']}", json=family_test_data["update_family"], headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "not found" in response.json()["message"].lower()

# def test_delete_family_success():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers)
#     family_id = create_resp.json()["family"]["id"]
#     response = client.delete(f"/api/v1/families/{family_id}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 1
#     assert "deleted" in response.json()["message"].lower()

# def test_delete_family_unauthorized():
#     headers1 = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     create_resp = client.post("/api/v1/families/", json=family_test_data["family1"], headers=headers1)
#     family_id = create_resp.json()["family"]["id"]
#     headers2 = create_and_login_user(family_test_data["user2"], family_test_data["user2_login"])
#     response = client.delete(f"/api/v1/families/{family_id}", headers=headers2)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "forbidden" in response.json()["message"].lower() or "not allowed" in response.json()["message"].lower()

# def test_delete_family_not_found():
#     headers = create_and_login_user(family_test_data["user1"], family_test_data["user1_login"])
#     response = client.delete(f"/api/v1/families/{family_test_data['garbage_uuid']}", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["code"] == 0
#     assert "not found" in response.json()["message"].lower()

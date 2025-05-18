import pytest
from fastapi.testclient import TestClient
from lib import create_user, login
from main import app

client = TestClient(app)

# Test data for user scenarios
user_test_data = {
    "valid_user": {"name": "Test User", "email": "testuser@example.com", "plain_password": "TestPass123"},
    "update_user": {"name": "Updated User", "plain_password": "NewPass456"},
    "invalid_user": {"name": "", "email": "notanemail", "plain_password": ""},
    "login": {"email": "testuser@example.com", "password": "TestPass123"},
    "invalid_login": {"email": "testuser@example.com", "password": "WrongPass"},
    "user1":{"name": "User1", "email": "user1@example.com", "plain_password": "Pass123!"},
    "user2":{"name": "User2", "email": "user2@example.com", "plain_password": "Pass456!"},
    "user2_login":{"email": "user2@example.com", "password": "Pass456!"},
    "user1_update":{"name": "Jassmine"},
    "failed_update":{"name": "Shakepear"},
    "garbage_uuid":"00000000-0000-0000-0000-000000000000",
}

def test_create_user_success():
    response = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"] == "SUCCESSFUL"
    assert response.json()["user"]["email"] == user_test_data["valid_user"]["email"]

def test_create_user_invalid_data():
    response = client.post("/api/v1/users/", json=user_test_data["invalid_user"])
    assert response.status_code == 422

def test_user_login_success():
    # Ensure user exists
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    response = client.post("/api/v1/users/login", json=user_test_data["login"])
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"].lower().startswith("success")
    assert "user_key" in response.json()
    assert response.json()["user_key"] is not None
    assert "authorization" in response.json()["user_key"]
    assert response.json()["user_key"]["authorization"].startswith("Bearer ")

def test_user_login_invalid_password():
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    response = client.post("/api/v1/users/login", json=user_test_data["invalid_login"])
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower().startswith("failed")
    assert response.json()["user_key"] is None

def test_get_current_user_info():
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    login_resp = client.post("/api/v1/users/login", json=user_test_data["login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"] == "SUCCESSFUL"
    assert "user" in response.json()
    assert "password" not in response.json()["user"]  # Password should not be returned
    assert response.json()["user"]["email"] == user_test_data["valid_user"]["email"]

def test_get_all_users():
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert "users" in response.json()
    assert len(response.json()["users"])>0

def test_get_user_by_id():
    create_resp = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    user_id = create_resp.json()["user"]["id"]
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == user_id

def test_update_user_success():
    create_resp = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    user_id = create_resp.json()["user"]["id"]
    login_resp = client.post("/api/v1/users/login", json=user_test_data["login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    response = client.put(f"/api/v1/users/{user_id}", json=user_test_data["update_user"], headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 1

def test_delete_user_success():
    create_resp = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    user_id = create_resp.json()["user"]["id"]
    login_resp = client.post("/api/v1/users/login", json=user_test_data["login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 1

def test_update_user_unauthorized():
    # Create two users
    create_resp1 = client.post("/api/v1/users/", json=user_test_data["user1"])
    user1_id = create_resp1.json()["user"]["id"]
    create_resp2 = client.post("/api/v1/users/", json=user_test_data["user2"])
    # Login as user2
    login_resp = client.post("/api/v1/users/login", json=user_test_data["user2_login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    # Try to update user1 as user2
    response = client.put(f"/api/v1/users/{user1_id}", json=user_test_data["user1_update"], headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower() == "failed"
    assert "forbidden" in response.json()["message"].lower()

def test_delete_user_unauthorized():
    # Create two users
    create_resp1 = client.post("/api/v1/users/", json=user_test_data["user1"])
    user1_id = create_resp1.json()["user"]["id"]
    create_resp2 = client.post("/api/v1/users/", json=user_test_data["user2"])
    # Login as user2
    login_resp = client.post("/api/v1/users/login", json=user_test_data["user2_login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    # Try to delete user1 as user2
    response = client.delete(f"/api/v1/users/{user1_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower() == "failed"
    assert "forbidden" in response.json()["message"].lower()

def test_update_not_found_user():
    # Create and login a user
    client.post("/api/v1/users/", json=user_test_data["user2"])
    login_resp = client.post("/api/v1/users/login", json=user_test_data["user2_login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    # Try to update a non-existing user
    response = client.put(f"/api/v1/users/{user_test_data.get('garbage_uuid')}", json=user_test_data["failed_update"], headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower() == "failed"
    assert "not found" in response.json()["message"].lower()

def test_delete_not_found_user():
    # Create and login a user
    client.post("/api/v1/users/", json=user_test_data["user2"])
    login_resp = client.post("/api/v1/users/login", json=user_test_data["user2_login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    # Try to delete a non-existing user
    response = client.delete(f"/api/v1/users/{user_test_data.get('garbage_uuid')}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower() == "failed"
    assert "not found" in response.json()["message"].lower()

def test_get_non_existing_user():
    response = client.get(f"/api/v1/users/{user_test_data.get('garbage_uuid')}")
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower() == "failed"
    assert "not found" in response.json()["message"].lower()


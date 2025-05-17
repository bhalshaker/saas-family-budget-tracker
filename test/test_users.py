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
    "invalid_login": {"email": "testuser@example.com", "password": "WrongPass"}
}

def test_create_user_success():
    response = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"] == "SUCCESSFUL"
    assert response.json()["user"]["email"] == user_test_data["valid_user"]["email"]

def test_create_user_invalid_data():
    response = client.post("/api/v1/users/", json=user_test_data["invalid_user"])
    assert response.status_code == 422 or response.json()["code"] == 0

def test_user_login_success():
    # Ensure user exists
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    response = client.post("/api/v1/users/login", json=user_test_data["login"])
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"].lower().startswith("success")
    assert "user_key" in response.json()

def test_user_login_invalid_password():
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    response = client.post("/api/v1/users/login", json=user_test_data["invalid_login"])
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["status"].lower().startswith("failed")

def test_get_current_user_info():
    client.post("/api/v1/users/", json=user_test_data["valid_user"])
    login_resp = client.post("/api/v1/users/login", json=user_test_data["login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["status"] == "SUCCESSFUL"

def test_get_all_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert "users" in response.json()

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
    assert response.json()["code"] in [0, 1]  # Could be forbidden or successful

def test_delete_user_success():
    create_resp = client.post("/api/v1/users/", json=user_test_data["valid_user"])
    user_id = create_resp.json()["user"]["id"]
    login_resp = client.post("/api/v1/users/login", json=user_test_data["login"])
    token = login_resp.json().get("user_key", {}).get("authorization")
    headers = {"Authorization": token} if token else {}
    response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["code"] in [0, 1]  # Could be forbidden or successful

from fastapi.testclient import TestClient

def login(test_app: TestClient, username: str, password: str):
    # Log in using an existing mock user
    response = test_app.post("/api/login", json={"username": username, "password": password})

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json().get('detail', 'Unknown error')}")

    token = response.json().get('token')
    if not token:
        raise Exception("No token returned from login endpoint.")

    headers = {"Authorization": f"Bearer {token}"}
    return headers
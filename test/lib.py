from fastapi.testclient import TestClient

def login(test_app: TestClient, email: str, password: str):
    # Attempt to log in with the provided credentials
    payload = {
        "email": email,
        "password": password
    }
    response = test_app.post("/api/v1/login", json=payload)

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json().get('detail', 'Unknown error')}")

    authorization = response.json().get('authorization')
    if not authorization:
        raise Exception("No token returned from login endpoint.")

    headers = {"Authorization": authorization}
    return headers

def create_user(test_app: TestClient, name:str, email:str, password:str):
    # Create a new user
    payload = {
        "name": name,
        "email": email,
        "plain_password": password
    }
    response = test_app.post("/api/v1/users", json=payload)

    if response.status_code != 200:
        raise Exception(f"User creation failed: {response.json().get('detail', 'Unknown error')}")

    return response

def create_family(test_app: TestClient, family_name:str, headers:dict):
    # Create a new family
    payload = { 
        "name": family_name
    }
    response = test_app.post("/api/v1/families", json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Family creation failed: {response.json().get('detail', 'Unknown error')}")

    return response.json()

def add_user_to_family(test_app: TestClient, family_id:str, user_id:str,role:str, headers:dict):
    # Add a user to a family
    payload = {
        "user_id": user_id,
        "role": role
    }
    response = test_app.post(f"/api/v1/families/{family_id}/users", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to add user to family: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_goal(test_app: TestClient, name: str, target_amount: float, due_date: str, headers: dict, saved_amount: float = 0.0):
    # Create a new goal
    payload = {
        "name": name,
        "target_amount": target_amount,
        "due_date": due_date,
        "saved_amount": saved_amount
    }
    response = test_app.post("/api/v1/families/{family_id}/goals", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Goal creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_category(test_app: TestClient, name: str, type_: str, family_id: str, headers: dict):
    # Create a new category
    payload = {
        "name": name,
        "type": type_,
        "family_id": family_id
    }
    response = test_app.post("//api/v1/families/{family_id}/categories", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Category creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_account(test_app: TestClient, name: str, type_: str, headers: dict, balance: float = 0.0):
    # Create a new account
    payload = {
        "name": name,
        "type": type_,
        "balance": balance
    }
    response = test_app.post("/api/v1/families/{family_id}/accounts", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Account creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_budget(test_app: TestClient, category_id: str, name: str, amount: float, start_date: str, end_date: str, headers: dict):
    # Create a new budget
    payload = {
        "category_id": category_id,
        "name": name,
        "amount": amount,
        "start_date": start_date,
        "end_date": end_date
    }
    response = test_app.post("/api/v1/families/{family_id}/budgets", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Budget creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_transaction(test_app: TestClient, category_id: str, account_id: str, amount: float, date: str, type_: str, headers: dict, description: str = None):
    # Create a new transaction
    payload = {
        "category_id": category_id,
        "account_id": account_id,
        "amount": amount,
        "date": date,
        "type": type_
    }
    if description is not None:
        payload["description"] = description
    response = test_app.post("/api/v1/families/{family_id}transactions", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Transaction creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_budget_transaction(test_app: TestClient, budget_id: str, transaction_id: str, assigned_amount: float, headers: dict):
    # Create a new budget transaction
    payload = {
        "budget_id": budget_id,
        "transaction_id": transaction_id,
        "assigned_amount": assigned_amount
    }
    response = test_app.post("/api/v1/families/{family_id}/budgettransactions", json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Budget transaction creation failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()

def create_attachment(test_app: TestClient, transaction_id: str, file_path: str, headers: dict):
    # Create a new attachment for a transaction
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        response = test_app.post(f"/api/v1/transactions/{transaction_id}/attachments", files=files, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Attachment upload failed: {response.json().get('detail', 'Unknown error')}")
    return response.json()
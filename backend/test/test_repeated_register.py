import pytest

@pytest.fixture
def existing_user_data(test_client):
    user_data = {
        "nombre": "existinguser",
        "email": "existing@example.com",
        "contrasena": "existingpassword"
    }
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, f"Failed to create existing user. Response: {response.json()}"
    return user_data

def test_register_repeated_user1(test_client, existing_user_data):
    duplicate_user_data = {
        "nombre": "duplicateuser",
        "email": existing_user_data["email"],
        "contrasena": "duplicatepassword"
    }
    response_duplicate = test_client.post("/usuario/", json=duplicate_user_data)
    assert response_duplicate.status_code == 404, f"Expected status code 400 for duplicate registration but got {response_duplicate.status_code}. Response: {response_duplicate.json()}"

def test_register_repeated_user2(test_client, existing_user_data):
    duplicate_user_data = {
        "nombre": existing_user_data["nombre"],
        "email": "duplicate@example.com",
        "contrasena": "duplicatepassword"
    }
    response_duplicate = test_client.post("/usuario/", json=duplicate_user_data)
    assert response_duplicate.status_code == 404, f"Expected status code 400 for duplicate registration but got {response_duplicate.status_code}. Response: {response_duplicate.json()}"
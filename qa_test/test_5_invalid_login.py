import pytest

@pytest.mark.parametrize("invalid_user_data", [
    {"email": "notexisting@example.com", "contrasena": "testpassword"},
	{"email": "test@example.com", "contrasena": "wrongpassword"},
	{"email": "test@gmail.com", "contrasena": ""},
	{"email": "", "contrasena": "password"},
	{"email": "", "contrasena": ""}
])

def test_valid_login(test_client, invalid_user_data):
    register_user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
    }
    response = test_client.post("/usuario/", json=register_user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/login/", json=invalid_user_data)
    response_data = response.json()
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}. Response: {response.json()}"

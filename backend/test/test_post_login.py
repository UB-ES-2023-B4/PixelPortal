from data.test_parameters import Parameters
import pytest

@pytest.mark.parametrize("register_user_data", Parameters().get_register_user_list())
def test_valid_login(test_client, register_user_data):
    user_data = register_user_data
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, response.json()
    login_user = {"email": user_data["email"], "contrasena": user_data["contrasena"]}
    response = test_client.post("/login/", json=user_data)
    assert response.status_code == 200, response.json()
    response_data = response.json()
    assert "access_token" in response_data.keys()
    assert "token_type" in response_data.keys()
    assert "username" in response_data.keys()
    assert register_user_data["nombre"] == response_data["username"]

@pytest.mark.parametrize("invalid_user_data", [
    {"email": "notexisting@example.com", "contrasena": "testpassword"},
	{"email": "test@example.com", "contrasena": "wrongpassword"},
	{"email": "test@gmail.com", "contrasena": ""},
	{"email": "", "contrasena": "password"},
	{"email": "", "contrasena": ""}
])
def test_invalid_login(test_client, invalid_user_data):
    register_user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
    }
    response = test_client.post("/usuario/", json=register_user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/login/", json=invalid_user_data)
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}. Response: {response.json()}"

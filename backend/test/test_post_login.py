import pytest

@pytest.mark.parametrize("register_user_data", [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
    {"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
    {"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"},
    {"nombre": "Pepe",          "email": "pepe@gmail.com",          "contrasena": "Qwer!234"}
])

def test_valid_login(test_client, register_user_data):
    response = test_client.post("/usuario/", json=register_user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()['access_token']['access_token']
    login_user_data={"email": register_user_data["email"], "contrasena": register_user_data["contrasena"]}
    response = test_client.post("/login/", json=login_user_data)
    response_data = response.json()
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
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
    response_data = response.json()
    assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}. Response: {response.json()}"

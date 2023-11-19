import pytest

@pytest.mark.parametrize("valid_user_data", [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
    {"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
    {"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"},
    {"nombre": "Pepe",          "email": "pepe@gmail.com",          "contrasena": "Qwer!234"}
])

def test_valid_register(test_client, valid_user_data):
    response = test_client.post("/usuario/", json=valid_user_data)
    response_data = response.json()
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    assert "access_token" in response_data.keys()
    assert "user" in response_data.keys()
    assert "nombre" in response_data["user"].keys()
    assert valid_user_data["nombre"] == response_data["user"]["nombre"]
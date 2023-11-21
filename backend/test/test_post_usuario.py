from data.test_parameters import Parameters
import pytest

@pytest.mark.parametrize("valid_user_data", Parameters().get_register_user_list())

def test_valid_register(test_client, valid_user_data):
    response = test_client.post("/usuario/", json=valid_user_data)
    response_data = response.json()
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    assert "access_token" in response_data.keys()
    assert "user" in response_data.keys()
    assert "nombre" in response_data["user"].keys()
    assert valid_user_data["nombre"] == response_data["user"]["nombre"]

@pytest.mark.parametrize("invalid_user_data", [
    {"nombre": "", 				"email": "nottest@example.com", 	"contrasena": "testpassword"},
	{"nombre": "failtest", 		"email": "", 						"contrasena": "testpassword"},
	{"nombre": "failtest2", 	"email": "nottest2@example.com", 	"contrasena": ""},
	{"nombre": "failtest4", 	"email": "bad_format", 				"contrasena": "testpassword"},
	{"nombre": "failtest5", 	"email": "bad_format@", 			"contrasena": "testpassword"},
	{"nombre": "failtest6",		"email": "bad_format@asdf",			"contrasena": "testpassword"},
	{"nombre": "failtest7", 	"email": "@bad.com", 				"contrasena": "testpassword"},
	{"nombre": "failtest8", 	"email": "bad_format@asdf.a", 		"contrasena": "testpassword"}
])

def test_invalid_register(test_client, invalid_user_data):
    response = test_client.post("/usuario/", json=invalid_user_data)
    assert response.status_code == 400, f"Expected status code 404 but got {response.status_code}. Response: {response.json()}"

def test_register_repeated_user1(test_client):
    existing_user_data = Parameters().get_test_user()
    Parameters().registerUser(test_client, existing_user_data)
    duplicate_user_data = {
        "nombre": "duplicateuser",
        "email": existing_user_data["email"],
        "contrasena": "duplicatepassword"
    }
    response_duplicate = test_client.post("/usuario/", json=duplicate_user_data)
    assert response_duplicate.status_code == 404, f"Expected status code 400 for duplicate registration but got {response_duplicate.status_code}. Response: {response_duplicate.json()}"

def test_register_repeated_user2(test_client):
    existing_user_data = Parameters().get_test_user()
    Parameters().registerUser(test_client, existing_user_data)
    duplicate_user_data = {
        "nombre": existing_user_data["nombre"],
        "email": "duplicate@example.com",
        "contrasena": "duplicatepassword"
    }
    response_duplicate = test_client.post("/usuario/", json=duplicate_user_data)
    assert response_duplicate.status_code == 404, f"Expected status code 400 for duplicate registration but got {response_duplicate.status_code}. Response: {response_duplicate.json()}"
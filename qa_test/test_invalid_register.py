import pytest

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

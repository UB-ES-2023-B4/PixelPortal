import pytest

@pytest.mark.parametrize("user_data", [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"}
])

@pytest.mark.parametrize("new_password", [
    {
        "current_password": "testpassword", 
        "new_password": "newpassword",
        "email": "nonExisting@example.com"
        },
    {
        "current_password": "testpassword",
		"new_password": "",
		"email": "test@example.com"
        },
    {
        "current_password": "incorrect_password",
		"new_password": "testpassword",
		"email": "test@example.com"
        },
    {
        "current_password": "testpassword",
		"new_password": "testpassword",
		"email": "test@example.com"
        }
])

def test_valid_change_password(test_client, user_data, new_password):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code != 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    

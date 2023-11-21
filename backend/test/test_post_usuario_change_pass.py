import pytest

@pytest.mark.parametrize("new_password", [
    {
        "current_password": "testpassword", 
        "new_password": "newpassword",
        "email": "test@example.com"
        },
    {
        "current_password": "testpassword",
		"new_password": "verylargenewpasswordhappychristmashappytoeveryonehappyhappyhappy",
		"email": "test@example.com"
        },
    {
        "current_password": "testpassword",
		"new_password": "PassWordC0mb1nedWH!T#SpeTialCh@r@cters",
		"email": "test@example.com"
        },
    {
        "current_password": "testpassword",
		"new_password": "SimplePassword1234",
		"email": "test@example.com"
        }
])

def test_valid_change_password(test_client, new_password):
    user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
	}
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert "access_token" in response.json().keys()

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

def test_invalid_change_password(test_client, new_password):
    user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
	}
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code != 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    
@pytest.mark.skip(reason="needs to be completed")
def test_repeated_change_password(test_client):
    user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
	}
    new_password = {
        "current_password": "testpassword",
		"new_password": "SimplePassword1234",
		"email": "test@example.com"
    }
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code != 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    pass
    

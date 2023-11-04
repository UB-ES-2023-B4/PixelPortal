import pytest

@pytest.mark.parametrize("user_data", [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"}
])

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

def test_valid_login(test_client, user_data, new_password):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()['access_token']['access_token']
    response = test_client.post("/usuario/change_pass", json=new_password)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert access_token == response.json()['access_token'], f"Expected {access_token} but got {response.json()['access_token']}. Response: {response.json()}"
    

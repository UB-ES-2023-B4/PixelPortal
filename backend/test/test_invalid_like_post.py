import pytest

@pytest.mark.parametrize("like_data", [
    {"usuario_id": "", "publicacion_id": ""},
    {"usuario_id": "", "publicacion_id": "2"},
    {"usuario_id": "1", "publicacion_id": ""},
    {"usuario_id": "39", "publicacion_id": "369"}
])

def test_invalid_post_like(test_client, like_data):
    user_data = {
        "nombre": "Jonadan",
        "email": "jona@hotmail.com",
        "contrasena": "Awsome123$"
        }

    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]

    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/likes", json=like_data, headers=headers)
    response_data = response.json()
    assert response.status_code != 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"

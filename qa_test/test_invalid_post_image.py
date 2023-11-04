import pytest

@pytest.mark.parametrize("image_data", [
    {
        "titulo": "",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[]",
        "imagen_url": "string"
    	},
    {
        "titulo": "string",
        "descripcion": "",
        "usuario_nombre": "string",
        "tags": "[]",
        "imagen_url": "string"
    	},
    {
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "",
        "tags": "[]",
        "imagen_url": "string"
    	},
    {
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[]",
        "imagen_url": ""
    	},
])

def test_invalid_post_image(test_client, image_data):
    user_data = {
        "nombre": "Jonadan",
        "email": "jona@hotmail.com",
        "contrasena": "Awsome123$"
        }
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"

    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]

    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/publicaciones", json=image_data, headers=headers)
    response_data = response.json()
    assert response.status_code != 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
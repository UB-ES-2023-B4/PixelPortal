import pytest

@pytest.mark.parametrize("image_data", [
    {
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[]",
        "imagen_url": "string"
    	},
	{
        "titulo": "",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[\"azul\"]",
        "imagen_url": "string"
		},
	{
        "titulo": "string",
        "descripcion": "",
        "usuario_nombre": "string",
        "tags": "[\"blanco y negro\"]",
        "imagen_url": "string"
    	},
	{
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "",
        "tags": "[\"gato\", \"perro\", \"pajaro\", \"lagarto\"]",
        "imagen_url": "string"
    	},
	{
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[\"el\", \"mejor\", \"de\", \"todos\"]",
        "imagen_url": ""
    }
])

def test_post_image(test_client, image_data):
    user_data = {"nombre": "Jonadan", "email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    test_client.post("/usuario/", json=user_data)
    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = test_client.post("/login", json=login_data)
    access_token = response.json()["access_token"]
    response = test_client.post("/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
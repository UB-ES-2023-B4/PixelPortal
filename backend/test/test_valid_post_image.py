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
        "titulo": "Tiiitulo con espacios entre medio",
        "descripcion": "string",
        "usuario_nombre": "string",
        "tags": "[\"azul\"]",
        "imagen_url": "string"
		},
	{
        "titulo": "lorem ipsum",
        "descripcion": """
		Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Nullam gravida odio nec diam consectetur, vel finibus lectus tincidunt. 
        Ut vulputate libero vel quam fringilla, nec dapibus dui consequat. 
        Aenean volutpat tellus eu libero cursus, vel posuere neque lacinia. 
        Suspendisse potenti. Quisque nec metus sit amet purus aliquam facilisis. 
        Integer lacinia erat vel lacus euismod, vitae tincidunt massa eleifend. 
        Donec ultricies, erat vel auctor venenatis, arcu lectus volutpat mi, 
        sit amet convallis mauris odio id nisl.
        """,
        "usuario_nombre": "string",
        "tags": "[\"blanco y negro\"]",
        "imagen_url": "string"
    	},
	{
        "titulo": "string",
        "descripcion": "string",
        "usuario_nombre": "Usuario tonto",
        "tags": "[\"gato\", \"perro\", \"pajaro\", \"lagarto\"]",
        "imagen_url": "string"
    	}
])

def test_post_image(test_client, image_data):
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
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
import pytest

image_data_list = [
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
]

def register_and_login(test_client):
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
    return access_token

def post_images(test_client, access_token, image_data):
    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/publicaciones", json=image_data, headers=headers)
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    return response_data['id']

@pytest.mark.parametrize("count", [0, 1, 2, 3])

def test_valid_get_publicaciones_by_id(test_client, count):
    access_token = register_and_login(test_client)
    valid_pb_id_list = []
    for image_data in image_data_list:
        valid_pb_id_list.append(post_images(test_client, access_token, image_data))
    response = test_client.get(f"/publicaciones/{valid_pb_id_list[count]}/")
    response_data = response.json()
    assert response.status_code == 200, response_data

def test_invalid_get_publicaciones_by_id(test_client):
    response = test_client.get(f"/publicaciones//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_publicaciones_by_id(test_client):
    access_token = register_and_login(test_client)
    for image_data in image_data_list:
        post_images(test_client, access_token, image_data)
    response = test_client.get(f"/publicaciones//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_publicaciones_by_id(test_client):
    access_token = register_and_login(test_client)
    for image_data in image_data_list:
        post_images(test_client, access_token, image_data)
    response = test_client.get(f"/publicaciones/anyinvalid/")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_publicaciones_by_id(test_client):
    access_token = register_and_login(test_client)
    for image_data in image_data_list:
        post_images(test_client, access_token, image_data)
    response = test_client.get(f"/publicaciones/00000000/")
    response_data = response.json()
    assert response.status_code != 200, response_data
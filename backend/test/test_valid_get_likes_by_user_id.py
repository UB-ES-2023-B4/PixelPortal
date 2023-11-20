import pytest
user_data = {
        "nombre": "Jonadan",
        "email": "jona@hotmail.com",
        "contrasena": "Awsome123$"
}

image_data_list = [
    {"titulo": "string1","descripcion": "string","usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string1"},
    {"titulo": "string2","descripcion": "string","usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string2"},
    {"titulo": "string3","descripcion": "string","usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string3"},
    {"titulo": "string4","descripcion": "string","usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string4"}
]
likes_data_list = [
    {"usuario_id": "1", "publicacion_id" : "1"},
	{"usuario_id": "1", "publicacion_id": "2"},
	{"usuario_id": "1", "publicacion_id": "3"},
	{"usuario_id": "1", "publicacion_id": "4"}
]

def login_user_post(test_client,user_data):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"

    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]
    user_id = response.json()["user_id"]
    return access_token,user_id #Para hacer los posts de like
def post_images(test_client, access_token, image_data):
    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/publicaciones", json=image_data, headers=headers)
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    return response_data['id']
@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_get_likes_by_user_id(test_client, count):
    access_token,user_id = login_user_post(test_client,user_data)
    valid_pb_id_list = []
    for image in image_data_list:
        valid_pb_id_list.append(post_images(test_client, access_token, image))   #Post de la imagen
    headers= {"Authorization": f"Bearer {access_token}"}
    #print("usuario_id",user_id, "publicacion_id", valid_pb_id_list[count])
    response = test_client.post("/likes/", json={"usuario_id":user_id, "publicacion_id": valid_pb_id_list[count]},
                                headers=headers)
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    response = test_client.get(f"/likes/user/{user_id}")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data

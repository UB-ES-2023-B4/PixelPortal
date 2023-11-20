import pytest
user_data = {
        "nombre": "Jonadan",
        "email": "jona@hotmail.com",
        "contrasena": "Awsome123$"
}
users_data = [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
    {"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
    {"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"}
]

image_data_list = [
    {"titulo": "string1","descripcion": "string","usuario_nombre": "Jonadan","tags": "[]","imagen_url": "string1"}
]
likes_data_list = [
    {"usuario_id": "1", "publicacion_id" : "1"},
	{"usuario_id": "2", "publicacion_id": "1"},
	{"usuario_id": "3", "publicacion_id": "1"},
	{"usuario_id": "4", "publicacion_id": "1"}
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
def register(test_client, user_data):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, response.json()
def post_images(test_client, access_token, image_data):
    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/publicaciones", json=image_data, headers=headers)
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    return response_data['id']
@pytest.mark.parametrize("count",[0])
def test_get_likes_publication(test_client,count):
    access_token,user_id = login_user_post(test_client,user_data)
    for user in users_data:
        register(test_client,user) #registramos los usuarios
    valid_pb_id_list = []
    for image in image_data_list:
        valid_pb_id_list.append(post_images(test_client, access_token, image))   #Post de la imagen
    headers= {"Authorization": f"Bearer {access_token}"}
    for like in likes_data_list:#post de los likes
        print("usuario_id",like["usuario_id"])
        response = test_client.post("/likes/", json={"usuario_id":like["usuario_id"], "publicacion_id": like["publicacion_id"]},
                                    headers=headers)
        response_data = response.json()
        assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    print(valid_pb_id_list[0])
    response = test_client.get(f"/likes/{valid_pb_id_list[0]}")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data

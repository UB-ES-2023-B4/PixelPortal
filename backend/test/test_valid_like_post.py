import pytest

user_data_list = [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
    {"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
    {"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"},
    {"nombre": "Pepe",          "email": "pepe@gmail.com",          "contrasena": "Qwer!234"}
]

def register(test_client, user_data):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, response.json()
    return response.json()['user']['id']

likes_data_list = [
    {"usuario_id": "1", "publicacion_id" : "1"},
	{"usuario_id": "1", "publicacion_id": "2"},
	{"usuario_id": "1", "publicacion_id": "3"},
	{"usuario_id": "1", "publicacion_id": "4"}
]
@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_post_like(test_client, count):
    user_id_list = []
    response = test_client.get(f"/usuario/{likes_data_list[count]}/")
    response_data = response.json()
    assert response.status_code == 200, response_data


    login_data = {"email": response.json()["email"], "contrasena": response.json()["contrasena"]}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]

    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/likes/", json=like_data, headers=headers)
    response_data = response.json()
    assert response.status_code == 200,  f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
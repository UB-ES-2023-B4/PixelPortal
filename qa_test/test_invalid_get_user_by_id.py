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

def user_id(test_client):
    for user_data in user_data_list:
        register(test_client, user_data)

def test_invalid_get_user_by_id1(test_client):
    response = test_client.get(f"/usuario//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id2(test_client):
    user_id(test_client)
    response = test_client.get(f"/usuario//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id3(test_client):
    user_id(test_client)
    response = test_client.get(f"/usuario/anyinvalid/")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id4(test_client):
    user_id(test_client)
    response = test_client.get(f"/usuario/00000000/")
    response_data = response.json()
    assert response.status_code != 200, response_data
    
    
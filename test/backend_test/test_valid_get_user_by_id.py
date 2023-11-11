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

@pytest.mark.parametrize("count", [0, 1, 2, 3])

def test_valid_get_user_by_id(test_client, count):
    user_id_list=[]
    for user_data in user_data_list:
        user_id_list.append(register(test_client, user_data))
    response = test_client.get(f"/usuario/{user_id_list[count]}/")
    response_data = response.json()
    assert response.status_code == 200, response_data
    
    
user_data_list = [
    {"nombre": "testuser",      "email": "test@example.com",        "contrasena": "testpassword"},
    {"nombre": "testuser2",     "email": "test@gmail.com",          "contrasena": "testpassword"},
    {"nombre": "testuser3",     "email": "test.ub@alumnes.ub.edu",  "contrasena": "testpassword"},
    {"nombre": "Pepe",          "email": "pepe@gmail.com",          "contrasena": "Qwer!234"}
]

def register(test_client, user_data):
    response = test_client.post("/usuario/", json=user_data)
    assert response.status_code == 200, response.json()

def test_get_users(test_client):
    for user_data in user_data_list:
        register(test_client, user_data)
    response = test_client.get("/usuarios/")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data
    assert len(response_data) == 4, response_data
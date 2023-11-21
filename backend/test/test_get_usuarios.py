from data.test_parameters import Parameters

def test_get_users(test_client):
    Parameters().registerUsers(test_client)
    response = test_client.get("/usuarios/")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data
    assert len(response_data) == 4, response_data
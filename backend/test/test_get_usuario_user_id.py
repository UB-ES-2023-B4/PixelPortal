from data.test_parameters import Parameters
import pytest

@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_valid_get_user_by_id(test_client, count):
    user_list = Parameters().get_register_user_list()
    user_id_list=[]
    for user_data in user_list:
        response = Parameters().registerUser(test_client, user_data)
        user_id_list.append(response.json()['user']['id'])
    response = test_client.get(f"/usuario/{user_id_list[count]}/")
    response_data = response.json()
    assert response.status_code == 200, response_data
def test_invalid_get_user_by_id1(test_client):
    response = test_client.get(f"/usuario//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id2(test_client):
    Parameters().registerUsers(test_client)
    response = test_client.get(f"/usuario//")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id3(test_client):
    Parameters().registerUsers(test_client)
    response = test_client.get(f"/usuario/anyinvalid/")
    response_data = response.json()
    assert response.status_code != 200, response_data

def test_invalid_get_user_by_id4(test_client):
    Parameters().registerUsers(test_client)
    response = test_client.get(f"/usuario/00000000/")
    response_data = response.json()
    assert response.status_code != 200, response_data
    
    
    
from data.test_parameters import Parameters
import pytest

@pytest.mark.parametrize("user_id", [2,3,4,5])
def test_follow_user(test_client, user_id):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()
	access_token = response_data['access_token']
	follower_id = 1

	Parameters().registerUsers(test_client)

	headers= {"Authorization": f"Bearer {access_token}"}
	response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
	assert response.status_code == 200, response.json()

def test_invalid_follow_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()
	access_token = response_data['access_token']
	user_id = 999

	Parameters().registerUsers(test_client)
	follower_id = 1

	headers= {"Authorization": f"Bearer {access_token}"}
	response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
	assert response.status_code != 200, response.json()

def test_repetead_follow_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()
	access_token = response_data['access_token']
	user_id = 2

	Parameters().registerUsers(test_client)
	follower_id = 1

	headers= {"Authorization": f"Bearer {access_token}"}
	response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
	assert response.status_code == 200, response.json()

	headers= {"Authorization": f"Bearer {access_token}"}
	response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
	assert response.status_code != 200, response.json()

@pytest.mark.skip(reason="not implemented authorization")
def test_unauthorized_follow_user(test_client):
	user_data = Parameters().get_test_user()
	Parameters().login(test_client, user_data)
	user_id = 2

	follower_user = Parameters().get_register_user_list()[0]
	Parameters().registerUser(test_client, follower_user)
	follower_id = 1

	response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}")
	assert response.status_code != 200, response.json()
	pass
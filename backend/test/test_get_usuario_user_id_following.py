from data.test_parameters import Parameters
import pytest

def test_get_following_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()
	access_token = response_data['access_token']
	follower_id = 1

	Parameters().registerUsers(test_client)

	headers= {"Authorization": f"Bearer {access_token}"}
	for user_id in range(2, 6):
		response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
		assert response.status_code == 200, response.json()

	response = test_client.get(f"/usuario/{follower_id}/following", headers=headers)
	response_data = response.json()
	assert response.status_code == 200, response_data
	assert len(response_data) == 4, response_data

@pytest.mark.skip(reason="not implemented authorization")
def test_unauthorized_get_following_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()
	access_token = response_data['access_token']
	follower_id = 1

	Parameters().registerUsers(test_client)

	headers= {"Authorization": f"Bearer {access_token}"}
	for user_id in range(2, 6):
		response = test_client.post(f"/usuario/{user_id}/follow/{follower_id}", headers=headers)
		assert response.status_code == 200, response.json()

	response = test_client.get(f"/usuario/{follower_id}/following")
	response_data = response.json()
	assert response.status_code != 200, response_data
	pass
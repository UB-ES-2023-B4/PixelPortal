from data.test_parameters import Parameters

def test_valid_delete_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response = test_client.request(method="DELETE", url="/usuario/1")
	assert response.status_code == 200, response.json()

def test_invalid_delete_user(test_client):
	response = test_client.request(method="DELETE", url="/usuario/1")
	assert response.status_code != 200, response.json()
from data.test_parameters import Parameters

def test_modify_user(test_client):
	user_data = Parameters().get_test_user()
	response = Parameters().login(test_client, user_data)
	response_data = response.json()

	access_token = response_data['access_token']
	username = response_data['username']
	new_description = "test description"
	new_img_url = "test_img.jpg"
	json_data = {
		"nombre": user_data['nombre'],
		"email": user_data['email'],
		"descripcion": new_description,
		"imagen_perfil_url": new_img_url
	}

	headers= {"Authorization": f"Bearer {access_token}"}
	response = test_client.put(f"/usuario/{username}", json=json_data, headers=headers)
	assert response.status_code == 200, response.json()

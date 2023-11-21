from data.test_parameters import Parameters

def test_valid_post_image(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']

    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users/me", headers=headers)
    response_data = response.json()
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
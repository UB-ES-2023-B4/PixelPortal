from data.test_parameters import Parameters

def test_valid_bookmark(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    for bookmark_data in Parameters().get_bookmark_data_list():
        Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    response = test_client.get("/bookmarks/user/1")
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert len(response.json()) == 4, response.json()

def test_valid_bookmark2(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    for bookmark_data in Parameters().get_bookmark_data_list():
        Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    
    user_data = Parameters().get_register_user_list()[0]
    response = Parameters().login(test_client, user_data)

    response = test_client.get("/bookmarks/user/2")
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert len(response.json()) == 0, response.json()

def test_invalid_bookmark(test_client):
    response = test_client.get("/bookmarks/user/2")
    assert response.status_code != 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
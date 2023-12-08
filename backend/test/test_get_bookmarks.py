from data.test_parameters import Parameters

def test_valid_bookmark(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    for bookmark_data in Parameters().get_bookmark_data_list():
        Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    response = test_client.get("/bookmarks")
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert len(response.json()) == 4, f"Expected length 4 but got {len(response.json())}"

def test_valid_empty_bookmark(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    response = test_client.get("/bookmarks")
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert len(response.json()) == 0, f"Expected length 0 but got {len(response.json())}"

def test_valid_empty_bookmark2(test_client):
    response = test_client.get("/bookmarks")
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    assert len(response.json()) == 0, f"Expected length 0 but got {len(response.json())}"
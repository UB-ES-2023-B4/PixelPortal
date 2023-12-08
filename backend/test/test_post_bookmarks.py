from data.test_parameters import Parameters
import pytest
@pytest.mark.parametrize("bookmark_data", [
    {
		"usuario_id": 1,
		"publicacion_id": 1
	},
    {
		"usuario_id": 1,
		"publicacion_id": 2
	},
    {
		"usuario_id": 1,
		"publicacion_id": 3
	}
])
def test_valid_bookmark(test_client, bookmark_data):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    response = Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"


@pytest.mark.parametrize("bookmark_data", [
    {
		"usuario_id": 1,
		"publicacion_id": 999
	},
    {
		"usuario_id": 999,
		"publicacion_id": 999
	}
])
def test_invalid_bookmark(test_client, bookmark_data):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    image_data = Parameters().get_image_data_list()[0]
    response = Parameters().post_image(test_client, access_token, image_data)
    response = Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    assert response.status_code != 200, \
        f"Expected status code 404 but got {response.status_code}. Response: {response.json()}"
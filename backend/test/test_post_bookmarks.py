from data.test_parameters import Parameters
import pytest

@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_valid_post_bookmarks(test_client, count):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    user_id = response.json()["user_id"]

    valid_pb_id_list = []
    for image_data in Parameters().get_image_data_list():
        response = Parameters().post_image(test_client, access_token, image_data)
        valid_pb_id_list.append(response.json()['id'])

    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/bookmarks/", json={"usuario_id": user_id, "publicacion_id": valid_pb_id_list[count]},
                                headers=headers)
    response_data = response.json()
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response_data}"


invalid_bookmarks_data_list = [
    {"usuario_id": "1", "publicacion_id": "1"},  # publicacion repetida
    {"usuario_id": "69", "publicacion_id": "23"},  # user no existe
    {"usuario_id": "1", "publicacion_id": "45"},  # Post no existe
    {"usuario_id": "35", "publicacion_id": "45"}  # user y post no existe
]


@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_invalid_post_bookmarks(test_client, count):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']

    valid_pb_id_list = []
    for image_data in Parameters().get_image_data_list():
        response = Parameters().post_image(test_client, access_token, image_data)
        valid_pb_id_list.append(response.json()['id'])

    headers = {"Authorization": f"Bearer {access_token}"}
    if count == 0:
        response = test_client.post("/bookmarks/",
                                    json={
                                        "usuario_id": invalid_bookmarks_data_list[count]['usuario_id'],
                                        "publicacion_id": invalid_bookmarks_data_list[count]['publicacion_id']
                                    },
                                    headers=headers)

    response = test_client.post("/bookmarks/",
                                json={
                                    "usuario_id": invalid_bookmarks_data_list[count]['usuario_id'],
                                    "publicacion_id": invalid_bookmarks_data_list[count]['publicacion_id']
                                },
                                headers=headers)
    response_data = response.json()
    assert response.status_code != 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
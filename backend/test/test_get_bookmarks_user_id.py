from data.test_parameters import Parameters
import pytest


def test_get_bookmarks_by_user_id(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    user_id = response.json()["user_id"]

    valid_pb_id_list = []
    for image_data in Parameters().get_image_data_list():
        response = Parameters().post_image(test_client, access_token, image_data)
        valid_pb_id_list.append(response.json()['id'])

    headers = {"Authorization": f"Bearer {access_token}"}
    for i in range(4):
        test_client.post("/bookmarks/", json={"usuario_id": user_id, "publicacion_id": valid_pb_id_list[i]},
                         headers=headers)
    response = test_client.get(f"/bookmarks/user/{user_id}")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data


invalid_bookmarks_data_list = [
    {"usuario_id": "69", "publicacion_id": "2"},  # user no existe
    {"usuario_id": "35", "publicacion_id": "45"}  # user y post no existe
]


@pytest.mark.parametrize("count", [0, 1])
def test_post_bookmarks(test_client, count):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    user_id = response.json()["user_id"]

    valid_pb_id_list = []
    for image_data in Parameters().get_image_data_list():
        response = Parameters().post_image(test_client, access_token, image_data)
        valid_pb_id_list.append(response.json()['id'])

    headers = {"Authorization": f"Bearer {access_token}"}
    for i in range(4):
        test_client.post("/bookmarks/", json={"usuario_id": user_id, "publicacion_id": valid_pb_id_list[i]},
                         headers=headers)
    response = test_client.get(f"/bookmarks/user/{invalid_bookmarks_data_list[count]['usuario_id']}")
    response_data = response.json()
    assert response.status_code != 200, response_data
    assert type(response_data) != type(list()), response_data

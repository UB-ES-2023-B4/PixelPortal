from data.test_parameters import Parameters
import pytest


@pytest.mark.parametrize("count", [0, 1, 2, 3])
def test_delete_bookmarks(test_client, count):
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

    response = test_client.request(method="DELETE",
                                   url="/bookmarks", headers=headers,
                                   json={
                                       "usuario_id": user_id,
                                       "publicacion_id": valid_pb_id_list[count],
                                       "fecha_creacion": "0"
                                   })
    response_data = response.json()
    assert response.status_code == 200, \
        f"Expected status code 200 but got {response.status_code}. Response: {response_data}"


@pytest.mark.parametrize("bookmarks_data", [
    {"usuario_id": "", "publicacion_id": ""},
    {"usuario_id": "", "publicacion_id": "2"},
    {"usuario_id": "1", "publicacion_id": ""},
    {"usuario_id": "39", "publicacion_id": "369"}  # Datos inválidos para borrar
])
def test_invalid_delete_bookmarks(test_client, bookmarks_data):
    user_data = Parameters().get_test_user()
    response = Parameters().registerUser(test_client, user_data)
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.request(method="DELETE", url="/bookmarks", headers=headers, json=bookmarks_data)
    response_data = response.json()

    assert response.status_code != 200, \
        f"Expected status code 404 but got {response.status_code}. Response: {response_data}"

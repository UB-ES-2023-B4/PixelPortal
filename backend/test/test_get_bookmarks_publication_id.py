from data.test_parameters import Parameters

def test_get_bookmarks_publication(test_client, ):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    user_id = response.json()["user_id"]

    Parameters().registerUsers(test_client)

    image_data = Parameters().get_image_data_list()[0]
    response = Parameters().post_image(test_client, access_token, image_data)
    p_id = response.json()['id']

    headers = {"Authorization": f"Bearer {access_token}"}
    for user_id in range(1, 5):  # post de los bookmarks
        response = test_client.post("/bookmarks/", json={"usuario_id": user_id, "publicacion_id": user_id},
                                    headers=headers)

    response = test_client.get(f"/bookmarks/{p_id}")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data


def test_invalid_get_bookmarks_publication(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    user_id = response.json()["user_id"]

    Parameters().registerUsers(test_client)

    image_data = Parameters().get_image_data_list()[0]
    Parameters().post_image(test_client, access_token, image_data)

    headers = {"Authorization": f"Bearer {access_token}"}
    for user_id in range(1, 5):  # post de los bookmarks
        response = test_client.post("/bookmarks/", json={"usuario_id": user_id, "publicacion_id": user_id},
                                    headers=headers)

    invalid_post_id = 39  # Id de post invalido
    response = test_client.get(f"/bookmarks/{invalid_post_id}")
    response_data = response.json()
    assert response.status_code != 200, response_data

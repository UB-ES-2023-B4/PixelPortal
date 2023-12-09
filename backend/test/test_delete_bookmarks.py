from data.test_parameters import Parameters

def test_valid_bookmark(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    for bookmark_data in Parameters().get_bookmark_data_list():
        Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    headers= {"Authorization": f"Bearer {access_token}"}
    for i in range(1, 5):
        response = test_client.request(method="DELETE",
                                        url="/bookmarks",
                                        headers=headers,
                                        json={
                                            "usuario_id":1,
                                            "publicacion_id":i,
                                            "fecha_creacion": "2023-12-09T15:42:33.292Z"
                                        })
        assert response.status_code == 200, response.json()

def test_invalid_bookmark(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.request(method="DELETE",
                                    url="/bookmarks",
                                    headers=headers,
                                    json={
                                        "usuario_id":1,
                                        "publicacion_id":1,
                                        "fecha_creacion": "2023-12-09T15:42:33.292Z"
                                    })
    assert response.status_code != 200, response.json()

def test_invalid_bookmark2(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
    for bookmark_data in Parameters().get_bookmark_data_list():
        Parameters().post_bookmarks(test_client, access_token, bookmark_data)
    headers= {"Authorization": f"Bearer {access_token}"}
    for i in range(1, 5):
        response = test_client.request(method="DELETE",
                                        url="/bookmarks",
                                        headers=headers,
                                        json={
                                            "usuario_id":1,
                                            "publicacion_id":i,
                                            "fecha_creacion": "2023-12-09T15:42:33.292Z"
                                        })
        assert response.status_code == 200, response.json()
    response = test_client.request(method="DELETE",
                                    url="/bookmarks",
                                    headers=headers,
                                    json={
                                        "usuario_id":1,
                                        "publicacion_id":1,
                                        "fecha_creacion": "2023-12-09T15:42:33.292Z"
                                    })
    assert response.status_code != 200, response.json()

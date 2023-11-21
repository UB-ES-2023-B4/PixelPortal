from data.test_parameters import Parameters

def test_get_likes_publication(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    
    Parameters().registerUsers(test_client)

    valid_pb_id_list = []
    for image_data in Parameters().get_image_data_list():
        response = Parameters().post_image(test_client, access_token, image_data)
        valid_pb_id_list.append(response.json()['id'])

    headers= {"Authorization": f"Bearer {access_token}"}
    for user_id in range(1, 5):#post de los likes
        response = test_client.post("/likes/", json={"usuario_id":user_id, "publicacion_id": 1},
                                    headers=headers)
        response_data = response.json()
        assert response.status_code == 200, \
            f"Expected status code 200 but got {response.status_code}. Response: {response_data}"

    response = test_client.get("/likes/")
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert type(response_data) == type(list()), response_data
    assert len(response_data) == 4, response_data


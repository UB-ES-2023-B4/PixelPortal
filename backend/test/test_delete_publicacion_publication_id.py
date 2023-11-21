from data.test_parameters import Parameters

def test_delete_publication_by_id(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
        
    headers= {"Authorization": f"Bearer {access_token}"}
    for i in range(1, 5):
        response = test_client.request(method="DELETE", url=f"/publicacion/{i}", headers=headers)
        assert response.status_code == 200, response.json()
        
def test_invalid_delete_publication_by_id(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
        
    headers= {"Authorization": f"Bearer {access_token}"}
    for i in range(1, 5):
        response = test_client.request(method="DELETE", url=f"/publicacion/{i}", headers=headers)
        assert response.status_code != 200, response.json()
        
def test_unauthorized_delete_publication_by_id(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = "invalid_token"
    
    for image_data in Parameters().get_image_data_list():
        Parameters().post_image(test_client, access_token, image_data)
        
    headers= {"Authorization": f"Bearer {access_token}"}
    for i in range(1, 5):
        response = test_client.request(method="DELETE", url=f"/publicacion/{i}", headers=headers)
        assert response.status_code != 200, response.json()
    
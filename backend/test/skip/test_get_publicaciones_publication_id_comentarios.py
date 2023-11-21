from data.test_parameters import Parameters
import pytest

@pytest.mark.skip(reason="unknown error on post comments")
def test_get_comments(test_client):
    user_data = Parameters().get_test_user()
    response = Parameters().login(test_client, user_data)
    access_token = response.json()['access_token']
    image_data = Parameters().get_image_data_list()[0]
    Parameters().post_image(test_client, access_token, image_data)
    
    for i in range(1, 4):
        response = Parameters().post_comment(test_client, access_token, 1, 1, f"test string{i}")
        assert response.status_code == 200, response.json()

    headers= {"Authorization": f"Bearer {access_token}"}
    response = test_client.get(url="/publicaciones/1/comentarios", headers=headers)
    pass
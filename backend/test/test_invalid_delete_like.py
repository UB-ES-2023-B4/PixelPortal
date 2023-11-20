import pytest

@pytest.mark.parametrize("like_data", [
    {"usuario_id": "", "publicacion_id": ""},
    {"usuario_id": "", "publicacion_id": "2"},
    {"usuario_id": "1", "publicacion_id": ""},
    {"usuario_id": "39", "publicacion_id": "369"}# Datos inválidos para borrar
])
def test_invalid_delete_like(test_client, like_data):
    register_user_data = {
        "nombre": "testuser",
        "email": "test@example.com",
        "contrasena": "testpassword"
    }
    response = test_client.post("/usuario/", json=register_user_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.request(method="DELETE", url="/likes", headers=headers, json=like_data)
    response_data = response.json()

    assert response.status_code != 200, f"Expected status code 404 but got {response.status_code}. Response: {response_data}"

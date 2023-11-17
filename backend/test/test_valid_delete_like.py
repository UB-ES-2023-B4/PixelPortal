import pytest

@pytest.mark.parametrize("like_data", [
    {"usuario_id": "1", "publicacion_id": "1"},
    {"usuario_id": "1", "publicacion_id": "2"},
    {"usuario_id": "1", "publicacion_id": "3"},
    {"usuario_id": "1", "publicacion_id": "4"} # Datos inválidos para borrar
])
def test_delete_like(test_client, like_data):
    # Suponiendo que se ha creado un like válido antes de esta prueba para poder borrarlo
    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = test_client.post("/login", json=login_data)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.json()}"
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.delete("/likes/", json=like_data, headers=headers)
    response_data = response.json()

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"
    """
    else:
        # En este caso se espera un error porque los datos para borrar son inválidos
        assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}. Response: {response_data}"
    """
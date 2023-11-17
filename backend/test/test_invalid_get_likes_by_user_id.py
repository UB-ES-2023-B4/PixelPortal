import pytest

# Asumiendo que tienes un usuario existente con ID 1 en la base de datos de prueba

def test_Invalid_get_likes_usert(test_client):
    invalit_users_id = [450,39,None,-9]  # Comprobamos que no hay likes en post que no existen

    for i in invalit_users_id:
        # Hacer una solicitud GET al endpoint con el ID del usuario
        response = test_client.get(f"/likes/{i}")
        assert response.status_code != 200, f"Expected status code 200 but got {response.status_code}. Response: {response_data}"        # Verificar que la respuesta sea una lista de publicaciones (o vacía si el usuario no tiene likes)

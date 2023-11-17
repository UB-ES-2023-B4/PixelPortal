import pytest

# Asumiendo que tienes un usuario existente con ID 1 en la base de datos de prueba

def test_get_likes_publication(test_client):
    posts_id = [1,2,3,4]  # Comprobamos los likes de los usuarios

    for i in posts_id:
        # Hacer una solicitud GET al endpoint con el ID del usuario
        response = test_client.get(f"/likes/{publication_id}")
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        # Verificar que la respuesta sea una lista de publicaciones (o vacía si el usuario no tiene likes)
        users = response.json()
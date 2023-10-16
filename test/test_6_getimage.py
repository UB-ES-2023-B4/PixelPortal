import requests
import json

API_URL = "http://localhost:8000"

access_token=None

imgdata_lst = list()

def test_start():
    user_data = {"nombre": "Jonadan", "email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    
    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    global access_token
    access_token = response_data["access_token"]

def test_getimage():
    user_data = {"nombre": "Jonadan", "email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    
    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    global access_token
    access_token = response_data["access_token"]
    
    response = requests.get(f"{API_URL}/publicaciones", headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert isinstance(response_data, list)
    assert response_data != 0
    for publicacion in response_data:
        assert "usuario_id" in publicacion
        assert "usuario_nombre" in publicacion
        assert "titulo" in publicacion
        assert "descripcion" in publicacion
        assert "imagen_url" in publicacion
        assert "id" in publicacion
        assert "fecha_creacion" in publicacion

import requests
import json

API_URL = "http://localhost:8000"

def test_register_user1():
    user_data = {
        "email": "test@example.com", 
        "contrasena": "testpassword"
        }
    response = requests.post(f"{API_URL}/login/", json=user_data)
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    assert "username" in response_data
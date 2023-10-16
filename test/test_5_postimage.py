import requests
import json

API_URL = "http://localhost:8000"

access_token=None

imgdata_lst = list()

def get_img_data(index):
    if (len(imgdata_lst) != 0):
        return imgdata_lst[index]
    f = open("test_postimage_image_list.txt")
    users_json = f.read().split("\n")
    for json_str in users_json:
        imgdata_lst.append(json.loads(json_str))
    return imgdata_lst[index]

def test_start():
    user_data = {"nombre": "Jonadan", "email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    
    login_data = {"email": "jona@hotmail.com", "contrasena": "Awsome123$"}
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    global access_token
    access_token = response_data["access_token"]

def test_postimage1():
    image_data=get_img_data(0)
    response = requests.post(f"{API_URL}/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 200, response_data

def test_postimage2():
    image_data=get_img_data(1)
    response = requests.post(f"{API_URL}/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_postimage3():
    image_data=get_img_data(2)
    response = requests.post(f"{API_URL}/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_postimage4():
    image_data=get_img_data(3)
    response = requests.post(f"{API_URL}/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_postimage5():
    image_data=get_img_data(4)
    response = requests.post(f"{API_URL}/publicaciones", json=image_data, headers={"Authorization": f"Bearer {access_token}"})
    response_data = response.json()
    assert response.status_code == 404, response_data

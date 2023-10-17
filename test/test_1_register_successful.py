import requests
import json

API_URL = "http://localhost:8000"
user_lst = list()

def get_user_data(index):
    if (len(user_lst) != 0):
        return user_lst[index]
    f = open("test_register_user_list_successful.txt")
    users_json = f.read().split("\n")
    for json_str in users_json:
        user_lst.append(json.loads(json_str))
    return user_lst[index]

def asserts(response):
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert "access_token" in response_data
    assert "user" in response_data

def test_register_user1():
    user_data = get_user_data(0)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_user2():
    user_data = get_user_data(1)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_user3():
    user_data = get_user_data(2)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_user4():
    user_data = get_user_data(3)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)
import requests
import json

API_URL = "http://localhost:8000"

user_list = list()

def get_user_data(index):
    if (len(user_list) != 0):
        return user_list[index]
    f = open("test_login_user_list_failure.txt")
    users_json = f.read().split("\n")
    for json_str in users_json:
        user_list.append(json.loads(json_str))
    return user_list[index]

def test_login_user1():
    login_data = get_user_data(0)
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_login_user2():
    login_data = get_user_data(1)
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_login_user3():
    login_data = get_user_data(2)
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_login_user4():
    login_data = get_user_data(3)
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    assert response.status_code == 404, response_data

def test_login_user5():
    login_data = get_user_data(4)
    response = requests.post(f"{API_URL}/login", json=login_data)
    response_data = response.json()
    assert response.status_code == 404, response_data
import requests
import json

API_URL = "http://localhost:8000"

user_lst = list()

def get_user_data(index):
    if (len(user_lst) != 0):
        return user_lst[index]
    f = open("test_login_user_list_successful.txt")
    users_json = f.read().split("\n")
    for json_str in users_json:
        user_lst.append(json.loads(json_str))
    return user_lst[index]

def asserts(response):
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    assert "username" in response_data

def test_login_user1():
    login_data = get_user_data(0)
    response = requests.post(f"{API_URL}/login", json=login_data)
    asserts(response)

def test_login_user2():
    login_data = get_user_data(1)
    response = requests.post(f"{API_URL}/login", json=login_data)
    asserts(response)

def test_login_user3():
    login_data = get_user_data(2)
    response = requests.post(f"{API_URL}/login", json=login_data)
    asserts(response)

def test_login_user4():
    login_data = get_user_data(3)
    response = requests.post(f"{API_URL}/login", json=login_data)
    asserts(response)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import json

TEST_SQLALQUEMY_URL="sqlite:///./test.db"
API_URL = "http://localhost:8000"
user_lst = list()
register_successful = "test_register_user_list_successful.txt"
register_failure = "test_register_user_list_failure.txt"

def get_user_data(index, filename):
    if (len(user_lst) != 0):
        return user_lst[index]
    f = open(filename)
    users_json = f.read().split("\n")
    for json_str in users_json:
        user_lst.append(json.loads(json_str))
    f.close()
    return user_lst[index]

def asserts(response):
    response_data = response.json()
    assert response.status_code == 200, response_data
    assert "access_token" in response_data
    assert "user" in response_data

def test_register_successful_user1():
    user_data = get_user_data(0, register_successful)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_successful_user2():
    user_data = get_user_data(1, register_successful)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_successful_user3():
    user_data = get_user_data(2, register_successful)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    asserts(response)

def test_register_successful_user4():
    user_data = get_user_data(3, register_successful)
    response = requests.post(f"{API_URL}/usuario/", json=user_data)
    user_lst.clear()
    asserts(response)
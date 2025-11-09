import time
import uuid

import pytest
import requests
from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def sample_user_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"client_{unique_id}@test.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "Client",
        "phone_number": f"12345444",
        "role": "client",
    }


@pytest.fixture(scope="function")
def sample_client_data():
    return {
        "first_name": "Test",
        "last_name": "Client",
        "phone_number": f"12345222",
        "address": f"Test Street 2",
    }


def create_user_via_api(user_data):
    try:
        response = requests.post("http://localhost:8000/users/register", json=user_data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error creating user: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API error: {e}")
        return None


def register_client_via_api(client_data, user_id):
    try:
        response = requests.post(
            f"http://localhost:8000/client/register?user_id={user_id}", json=client_data
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error registering client: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API error: {e}")
        return None


def cleanup_test_data(user_id, email):
    try:
        requests.delete(f"http://localhost:8000/client/{user_id}")
        requests.delete(f"http://localhost:8000/users/delete/{email}")
    except Exception:
        pass


@pytest.fixture(scope="function")
def authenticated_driver(driver, sample_user_data, sample_client_data):
    user_data = sample_user_data

    user = create_user_via_api(user_data)
    assert user is not None

    user_id = user["id"]

    client_data = sample_client_data

    client = register_client_via_api(client_data, user_id)
    assert client is not None
    login_page = LoginPage(driver)
    login_page.open("http://localhost:3000")
    login_page.login_attempt(user_data["email"], user_data["password"])

    time.sleep(3)
    token = driver.execute_script("return localStorage.getItem('token');")
    assert token is not None

    yield driver
    cleanup_test_data(user_id, user_data["email"])

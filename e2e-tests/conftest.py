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


@pytest.fixture(scope="function")
def sample_registration_data():
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User",
        "phone": "123456789",
        "address": "Test Street 123"
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


def register_client_via_api(user_data, client_data):
    try:
        payload = {
            "user_data": user_data,
            "client": client_data
        }
        response = requests.post(
            "http://localhost:8000/client/register", 
            json=payload
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error registering client: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API error: {e}")
        return None

@pytest.fixture(scope="function")
def authenticated_driver(driver, sample_user_data, sample_client_data):
    user_data = sample_user_data
    client_data = sample_client_data

    client = register_client_via_api(user_data, client_data)
    assert client is not None
    login_page = LoginPage(driver)
    login_page.open("http://localhost:3000")
    login_page.login_attempt(user_data["email"], user_data["password"])

    time.sleep(3)
    token = driver.execute_script("return localStorage.getItem('token');")
    assert token is not None

    yield driver
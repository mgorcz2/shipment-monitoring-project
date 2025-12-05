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
        "phone_number": "12345222",
        "address": "Test Street 2",
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
        "address": "Test Street 123",
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
        payload = {"user_data": user_data, "client": client_data}
        response = requests.post("http://localhost:8000/client/register", json=payload)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error registering client: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API error: {e}")
        return None


def create_package_via_api(token, package_data):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            "http://localhost:8000/packages/add", json=package_data, headers=headers
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"Error creating package: {response.status_code} - {response.text}")
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

    yield driver


@pytest.fixture(scope="module")
def authenticated_manager_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    unique_id = str(uuid.uuid4())[:8]
    manager_user_data = {
        "email": f"manager_{unique_id}@test.com",
        "password": "ManagerPassword123!",
        "role": "manager",
    }

    create_user_via_api(manager_user_data)
    login_page = LoginPage(driver)
    login_page.open("http://localhost:3000")
    login_page.login_attempt(manager_user_data["email"], manager_user_data["password"])

    time.sleep(3)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def manager_with_package(authenticated_manager_driver):
    from pages.create_package_page import CreatePackagePage

    driver = authenticated_manager_driver
    package_page = CreatePackagePage(driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Krakowska",
        "number": "1",
        "city": "Warszawa",
        "postcode": "00-001",
    }

    destination = {
        "street": "Marszałkowska",
        "number": "10",
        "city": "Warszawa",
        "postcode": "00-590",
    }

    package_data = {
        "weight": 5,
        "length": 30,
        "width": 20,
        "height": 10,
        "fragile": False,
    }

    recipient_email = f"manager_test_{str(uuid.uuid4())[:8]}@test.com"

    package_page.create_full_package(origin, destination, recipient_email, package_data)
    time.sleep(3)

    yield driver


@pytest.fixture(scope="module")
def authenticated_admin_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    unique_id = str(uuid.uuid4())[:8]

    admin_user_data = {
        "email": f"admin_{unique_id}@test.com",
        "password": "Test1234!",
        "role": "admin",
    }
    admin_user = create_user_via_api(admin_user_data)
    assert admin_user is not None

    client_user_data = {
        "email": f"client_{unique_id}@test.com",
        "password": "Test1234!",
        "role": "client",
    }
    client_data = {
        "first_name": "Test",
        "last_name": "Client",
        "phone_number": "123456789",
        "address": "Test Street 1",
    }
    register_client_via_api(client_user_data, client_data)

    courier_user_data = {
        "email": f"courier_{unique_id}@test.com",
        "password": "Test1234!",
        "role": "courier",
    }
    create_user_via_api(courier_user_data)

    login_page = LoginPage(driver)
    login_page.open("http://localhost:3000")
    login_page.enter_email(admin_user_data["email"])
    login_page.enter_password(admin_user_data["password"])
    login_page.click_login()
    time.sleep(2)

    yield driver
    driver.quit()

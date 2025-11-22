import json
import time

from conftest import register_client_via_api
from pages.login_page import LoginPage

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"


def test_login_page_loads(driver):
    """Test that login page loads correctly"""
    login_page = LoginPage(driver)
    login_page.open(FRONTEND_URL)

    assert "login" in driver.current_url.lower()

    email_field = driver.find_element(*login_page.email_input)
    password_field = driver.find_element(*login_page.password_input)
    login_button = driver.find_element(*login_page.login_button)

    assert email_field.is_displayed()
    assert password_field.is_displayed()
    assert login_button.is_displayed()


def test_fake_login_attempt(driver):
    """Test login with invalid credentials"""
    login_page = LoginPage(driver)
    login_page.open(FRONTEND_URL)

    fake_email = "nieistnieje@test.com"
    fake_password = "WrongPassword123!"

    login_page.login_attempt(fake_email, fake_password)
    time.sleep(3)

    current_url = driver.current_url
    token = driver.execute_script("return localStorage.getItem('token');")
    assert "/login" in current_url
    assert token is None


def test_client_login(driver, sample_user_data, sample_client_data):
    """Test successful client login"""
    user_data = sample_user_data
    client_data = sample_client_data

    client = register_client_via_api(user_data, client_data)
    assert client is not None

    login_page = LoginPage(driver)
    login_page.open(FRONTEND_URL)
    login_page.login_attempt(user_data["email"], user_data["password"])

    time.sleep(5)

    token = driver.execute_script("return localStorage.getItem('token');")
    user_storage = driver.execute_script("return localStorage.getItem('user');")
    client_storage = driver.execute_script(
        "return localStorage.getItem('client_data');"
    )

    assert token is not None
    assert user_storage is not None

    if user_storage:
        user_obj = json.loads(user_storage)
        assert user_obj["email"] == user_data["email"]
        assert user_obj["role"] == "client"

    if client_storage:
        client_obj = json.loads(client_storage)
        assert client_obj["first_name"] == client_data["first_name"]
        assert client_obj["last_name"] == client_data["last_name"]

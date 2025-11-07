import json
import time
import uuid

import pytest
import requests
from conftest import cleanup_test_data, create_user_via_api, register_client_via_api
from pages.login_page import LoginPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()

        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"

        yield

        self.driver.quit()

    def test_login_page_loads(self):
        login_page = LoginPage(self.driver)
        login_page.open(self.frontend_url)

        assert "login" in self.driver.current_url.lower()

        email_field = self.driver.find_element(*login_page.email_input)
        password_field = self.driver.find_element(*login_page.password_input)
        login_button = self.driver.find_element(*login_page.login_button)

        assert email_field.is_displayed()
        assert password_field.is_displayed()
        assert login_button.is_displayed()

    def test_fake_login_attempt(self):
        login_page = LoginPage(self.driver)
        login_page.open(self.frontend_url)

        fake_email = "nieistnieje@test.com"
        fake_password = "WrongPassword123!"

        login_page.login_attempt(fake_email, fake_password)
        time.sleep(3)

        current_url = self.driver.current_url
        token = self.driver.execute_script("return localStorage.getItem('token');")
        assert "/login" in current_url
        assert token is None

    def test_client_registration_and_login(self, sample_user_data, sample_client_data):
        user_data = sample_user_data

        user = create_user_via_api(user_data)
        assert user is not None

        user_id = user["id"]

        client_data = sample_client_data

        client = register_client_via_api(client_data, user_id)
        assert client is not None

        login_page = LoginPage(self.driver)
        login_page.open(self.frontend_url)
        login_page.login_attempt(user_data["email"], user_data["password"])

        time.sleep(5)

        current_url = self.driver.current_url
        token = self.driver.execute_script("return localStorage.getItem('token');")
        user_storage = self.driver.execute_script(
            "return localStorage.getItem('user');"
        )
        client_storage = self.driver.execute_script(
            "return localStorage.getItem('client_data');"
        )

        assert "/login" not in current_url
        assert token is not None
        assert user_storage is not None

        if user_storage:
            user_obj = json.loads(user_storage)
            assert user_obj["email"] == user_data["email"]
            assert user_obj["role"] == "client"

        if client_storage:
            client_obj = json.loads(client_storage)
            assert client_obj["address"] == client_data["address"]

        cleanup_test_data(user_id, user_data["email"])

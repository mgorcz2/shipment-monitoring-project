import pytest
import time
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.register_page import RegisterPage
from conftest import create_user_via_api


class TestRegister:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        self.frontend_url = "http://localhost:3000"
        self.backend_url = "http://localhost:8000"
        
        yield
        
        self.driver.quit()

    def test_successful_registration(self, sample_registration_data):
        test_data = sample_registration_data
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        
        register_page.register_attempt(
            test_data["email"],
            test_data["password"], 
            test_data["first_name"],
            test_data["last_name"],
            test_data["phone"],
            test_data["address"]
        )
        
        success_message = register_page.wait_for_success(timeout=10)
        assert success_message is not None
        assert "sukcesem" in success_message or "success" in success_message.lower()
        
        time.sleep(3)
        current_url = self.driver.current_url

    
    def test_registration_with_existing_email(self, sample_registration_data):
        existing_email = sample_registration_data["email"]
        
        sample_registration_data["email"] = existing_email
        create_user_via_api(sample_registration_data)
    
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        
        register_page.register_attempt(
            existing_email,
            "Password123!",
            "Another",
            "User", 
            "987654321",
            "Another Street 456"
        )
        

        error_message = register_page.wait_for_error(timeout=5)
        
        assert error_message is not None
        assert "already registered" in error_message.lower()
    
    def test_registration_with_invalid_data(self):
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        
        register_page.register_attempt(
            "mail@example.com",  
            "string123",  
            "aaa",             
            "ss",             
            "abc",           
            "aaa"             
        )
        
        error_message = register_page.wait_for_error(timeout=5)
        assert error_message is not None
        
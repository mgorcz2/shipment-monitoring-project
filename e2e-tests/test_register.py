import pytest
import time
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.register_page import RegisterPage
from conftest import cleanup_test_data, create_user_via_api, register_client_via_api


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


    def test_register_page_loads(self):
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        
        assert "register" in self.driver.current_url.lower()
        
        email_field = self.driver.find_element(*register_page.email_input)
        password_field = self.driver.find_element(*register_page.password_input)
        first_name_field = self.driver.find_element(*register_page.first_name_input)
        last_name_field = self.driver.find_element(*register_page.last_name_input)
        phone_field = self.driver.find_element(*register_page.phone_input)
        address_field = self.driver.find_element(*register_page.address_input)
        register_btn = self.driver.find_element(*register_page.register_button)
        
        assert email_field.is_displayed()
        assert password_field.is_displayed()
        assert first_name_field.is_displayed()
        assert last_name_field.is_displayed()
        assert phone_field.is_displayed()
        assert address_field.is_displayed()
        assert register_btn.is_displayed()
        

    def test_empty_form_validation(self):
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        register_page.click_register()
        
        time.sleep(1)
        current_url = self.driver.current_url
        assert "register" in current_url

    def test_invalid_email_validation(self):
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        register_page.fill_email("invalid-email")
        register_page.click_register()
        time.sleep(1)
        
        email_field = self.driver.find_element(*register_page.email_input)
        email_valid = self.driver.execute_script("return arguments[0].validity.valid;", email_field)
        email_message = self.driver.execute_script("return arguments[0].validationMessage;", email_field)
        
        assert not email_valid
        assert "email" in email_message.lower() or "@" in email_message
            
    
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
            "123",           
            "aaa",             
            "ss",             
            "abc",           
            "aaa"             
        )
        
        error_message = register_page.wait_for_error(timeout=5)
        assert error_message is not None

    
    def test_form_field_validation(self):
        register_page = RegisterPage(self.driver)
        register_page.open(self.frontend_url)
        
        register_page.click_register()

        email_field = self.driver.find_element(*register_page.email_input)
        password_field = self.driver.find_element(*register_page.password_input)
        
        email_valid = self.driver.execute_script("return arguments[0].validity.valid;", email_field)
        password_valid = self.driver.execute_script("return arguments[0].validity.valid;", password_field)

        assert not email_valid
        assert not password_valid
        
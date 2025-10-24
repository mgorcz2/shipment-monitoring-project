import pytest
import time
import requests
import json
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage

class TestLogin:
    
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
    
    def create_user_via_api(self, user_data):
        try:
            response = requests.post(
                f"{self.backend_url}/users/register",
                json=user_data
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error creating user: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"API error: {e}")
            return None
    
    def register_client_via_api(self, client_data, user_id):
        try:
            response = requests.post(
                f"{self.backend_url}/client/register?user_id={user_id}",
                json=client_data
            )
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"Error registering client: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"API error: {e}")
            return None
    
    def cleanup_test_data(self, user_id, email):
        try:
            requests.delete(f"{self.backend_url}/client/{user_id}")
            requests.delete(f"{self.backend_url}/users/delete/{email}")
        except:
            pass
    
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
        
        print("Login page loaded successfully")
    
    def test_fake_login_attempt(self):
        login_page = LoginPage(self.driver)
        login_page.open(self.frontend_url)
        
        fake_email = "nieistnieje@test.com"
        fake_password = "WrongPassword123!"
        
        login_page.login_attempt(fake_email, fake_password)
        time.sleep(3)
        
        current_url = self.driver.current_url
        token = self.driver.execute_script("return localStorage.getItem('token');")
        
        print(f"Current URL: {current_url}")
        print(f"Token: {token}")
        
        assert "/login" in current_url
        assert token is None
        
        print("Fake login test passed")
    
    def test_client_registration_and_login(self):
        unique_id = str(uuid.uuid4())[:8]
        user_data = {
            "email": f"client_{unique_id}@test.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "Client", 
            "phone_number": f"12345444",
            "role": "client"
        }
        
        print(f"Creating user: {user_data['email']}")
        user = self.create_user_via_api(user_data)
        assert user is not None, "Failed to create user"
        
        user_id = user["id"]
        print(f"User created with ID: {user_id}")
        
        client_data = {
            "first_name": "Test",
            "last_name": "Client",
            "phone_number": f"12345222",
            "address": f"Test Street {unique_id[:4]}"
        }
        
        print("Registering client...")
        client = self.register_client_via_api(client_data, user_id)
        assert client is not None, "Failed to register client"
        
        print("Testing login via UI...")
        login_page = LoginPage(self.driver)
        login_page.open(self.frontend_url)
        login_page.login_attempt(user_data["email"], user_data["password"])
        
        time.sleep(5)
        
        current_url = self.driver.current_url
        token = self.driver.execute_script("return localStorage.getItem('token');")
        user_storage = self.driver.execute_script("return localStorage.getItem('user');")
        client_storage = self.driver.execute_script("return localStorage.getItem('client_data');")
        
        print(f"Login result - URL: {current_url}")
        print(f"Token present: {token is not None}")
        print(f"User data present: {user_storage is not None}")
        print(f"Client data present: {client_storage is not None}")
        
        assert "/login" not in current_url, "Should be redirected from login page"
        assert token is not None, "Token should be present"
        assert user_storage is not None, "User data should be present"
        
        if user_storage:
            user_obj = json.loads(user_storage)
            assert user_obj["email"] == user_data["email"], "User email should match"
            assert user_obj["role"] == "client", "User role should be client"
        
        if client_storage:
            client_obj = json.loads(client_storage)
            assert client_obj["address"] == client_data["address"], "Client address should match"
        
        print("Client registration and login test passed")
        self.cleanup_test_data(user_id, user_data["email"])
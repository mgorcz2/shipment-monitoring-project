import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        self.email_input = (By.ID, "email-input")
        self.password_input = (By.ID, "password-input")
        self.login_button = (By.ID, "login-submit-button")
        self.error_message = (By.CSS_SELECTOR, ".login-error")
        self.register_button = (By.CSS_SELECTOR, "button.btn-outline")
    
    def open(self, base_url):
        self.driver.get(f"{base_url}/login")
        time.sleep(1)
        return self
    
    def enter_email(self, email):
        email_field = self.driver.find_element(*self.email_input)
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.5)
        return self
    
    def enter_password(self, password):
        password_field = self.driver.find_element(*self.password_input)
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)
        return self
    
    def click_login(self):
        login_btn = self.driver.find_element(*self.login_button)
        login_btn.click()
        time.sleep(1)
        return self
    
    def login_attempt(self, email, password):
        return (self.enter_email(email)
                    .enter_password(password)
                    .click_login())
    
    def get_error_message(self):
        try:
            error_element = self.wait.until(EC.presence_of_element_located(self.error_message))
            return error_element.text
        except:
            return None
    
    def is_loading(self):
        try:
            login_btn = self.driver.find_element(*self.login_button)
            return "Logowanie..." in login_btn.text
        except:
            return False
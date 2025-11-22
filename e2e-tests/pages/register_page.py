import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.email_input = (By.CSS_SELECTOR, "input[name='email']")
        self.password_input = (By.CSS_SELECTOR, "input[name='password']")
        self.first_name_input = (By.CSS_SELECTOR, "input[name='first_name']")
        self.last_name_input = (By.CSS_SELECTOR, "input[name='last_name']")
        self.phone_input = (By.CSS_SELECTOR, "input[name='phone_number']")
        self.address_input = (By.CSS_SELECTOR, "input[name='address']")
        self.register_button = (By.CSS_SELECTOR, "button[type='submit']")

        self.error_message = (By.CSS_SELECTOR, ".register-error")
        self.success_message = (By.CSS_SELECTOR, ".register-success")
        self.loading_indicator = (
            By.XPATH,
            "//button[contains(text(), 'Rejestracja...')]",
        )

    def open(self, base_url):
        self.driver.get(f"{base_url}/register-client")
        time.sleep(1)
        return self

    def fill_email(self, email):
        email_field = self.driver.find_element(*self.email_input)
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.3)
        return self

    def fill_password(self, password):
        password_field = self.driver.find_element(*self.password_input)
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.3)
        return self

    def fill_first_name(self, first_name):
        first_name_field = self.driver.find_element(*self.first_name_input)
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        time.sleep(0.3)
        return self

    def fill_last_name(self, last_name):
        last_name_field = self.driver.find_element(*self.last_name_input)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        time.sleep(0.3)
        return self

    def fill_phone(self, phone):
        phone_field = self.driver.find_element(*self.phone_input)
        phone_field.clear()
        phone_field.send_keys(phone)
        time.sleep(0.3)
        return self

    def fill_address(self, address):
        address_field = self.driver.find_element(*self.address_input)
        address_field.clear()
        address_field.send_keys(address)
        time.sleep(0.3)
        return self

    def click_register(self):
        register_btn = self.driver.find_element(*self.register_button)
        register_btn.click()
        time.sleep(1)
        return self

    def register_attempt(self, email, password, first_name, last_name, phone, address):
        return (
            self.fill_email(email)
            .fill_password(password)
            .fill_first_name(first_name)
            .fill_last_name(last_name)
            .fill_phone(phone)
            .fill_address(address)
            .click_register()
        )

    def get_error_element(self, timeout=5):
        """Get error message element"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.error_message)
        )

    def get_success_element(self, timeout=10):
        """Get success message element"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.success_message)
        )

    def get_loading_element(self):
        """Get loading indicator element"""
        return self.driver.find_element(*self.loading_indicator)

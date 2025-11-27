from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProfilePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url="http://localhost:3000/profile"):
        self.driver.get(url)
        return self

    def get_edit_button(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-edit"))
        )

    def click_edit_button(self):
        self.get_edit_button().click()
        return self

    def get_first_name_input(self):
        return self.driver.find_element(By.NAME, "first_name")

    def get_last_name_input(self):
        return self.driver.find_element(By.NAME, "last_name")

    def get_phone_number_input(self):
        return self.driver.find_element(By.NAME, "phone_number")

    def get_address_input(self):
        return self.driver.find_element(By.NAME, "address")

    def fill_first_name(self, first_name):
        input_field = self.get_first_name_input()
        input_field.clear()
        input_field.send_keys(first_name)
        return self

    def fill_last_name(self, last_name):
        input_field = self.get_last_name_input()
        input_field.clear()
        input_field.send_keys(last_name)
        return self

    def fill_phone_number(self, phone):
        input_field = self.get_phone_number_input()
        input_field.clear()
        input_field.send_keys(phone)
        return self

    def fill_address(self, address):
        input_field = self.get_address_input()
        input_field.clear()
        input_field.send_keys(address)
        return self

    def get_save_button(self):
        return self.driver.find_element(By.CLASS_NAME, "btn-save")

    def get_cancel_button(self):
        return self.driver.find_element(By.CLASS_NAME, "btn-cancel")

    def click_save_button(self):
        self.get_save_button().click()
        return self

    def click_cancel_button(self):
        self.get_cancel_button().click()
        return self

    def get_success_alert(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

    def get_error_alert(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-error"))
        )

    def get_delete_account_button(self):
        return self.driver.find_element(By.CLASS_NAME, "btn-delete-account")

    def click_delete_account_button(self):
        self.get_delete_account_button().click()
        return self

    def get_modal_overlay(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-overlay"))
        )

    def get_modal_close_button(self):
        return self.driver.find_element(By.CLASS_NAME, "modal-close-btn")

    def get_delete_confirm_button(self):
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "Usuń konto na zawsze" in button.text:
                return button
        return None

    def get_first_name_value(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "info-item")))
        items = self.driver.find_elements(By.CLASS_NAME, "info-item")
        for item in items:
            label = item.find_element(By.TAG_NAME, "label")
            if "IMI" in label.text.upper():
                value = item.find_element(By.CLASS_NAME, "info-value")
                return value.text
        return None

    def get_last_name_value(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "info-item")))
        items = self.driver.find_elements(By.CLASS_NAME, "info-item")
        for item in items:
            label = item.find_element(By.TAG_NAME, "label")
            if "NAZWISKO" in label.text.upper():
                value = item.find_element(By.CLASS_NAME, "info-value")
                return value.text
        return None

    def get_phone_value(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "info-item")))
        items = self.driver.find_elements(By.CLASS_NAME, "info-item")
        for item in items:
            label = item.find_element(By.TAG_NAME, "label")
            if "TELEFON" in label.text.upper():
                value = item.find_element(By.CLASS_NAME, "info-value")
                return value.text
        return None

    def get_address_value(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "info-item")))
        items = self.driver.find_elements(By.CLASS_NAME, "info-item")
        for item in items:
            label = item.find_element(By.TAG_NAME, "label")
            if "ADRES" in label.text.upper():
                value = item.find_element(By.CLASS_NAME, "info-value")
                return value.text
        return None

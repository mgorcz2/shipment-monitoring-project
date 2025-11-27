from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class AdminPanelPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url="http://localhost:3000/admin"):
        self.driver.get(url)
        return self

    def get_user_table(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "user-table"))
        )

    def get_all_table_rows(self):
        table = self.get_user_table()
        return table.find_elements(By.TAG_NAME, "tbody")[0].find_elements(
            By.TAG_NAME, "tr"
        )

    def get_register_staff_button(self):
        return self.driver.find_element(By.CLASS_NAME, "btn-primary")

    def click_register_staff_button(self):
        self.get_register_staff_button().click()
        return self

    def get_role_filter(self):
        return self.driver.find_element(By.ID, "role-filter")

    def set_role_filter(self, role):
        select_element = Select(self.get_role_filter())
        select_element.select_by_value(role)
        return self

    def click_details_button(self, row_index=0):
        rows = self.get_all_table_rows()
        details_btn = rows[row_index].find_element(By.CLASS_NAME, "details-btn")
        details_btn.click()
        return self

    def click_edit_button(self, row_index=0):
        rows = self.get_all_table_rows()
        edit_btn = rows[row_index].find_element(By.CLASS_NAME, "edit-btn")
        edit_btn.click()
        return self

    def click_delete_button(self, row_index=0):
        rows = self.get_all_table_rows()
        delete_btn = rows[row_index].find_element(By.CLASS_NAME, "delete-btn")
        delete_btn.click()
        return self

    def get_modal_overlay(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-overlay"))
        )

    def get_modal_close_button(self):
        return self.driver.find_element(By.CLASS_NAME, "modal-close-btn")

    def click_modal_close_button(self):
        self.get_modal_close_button().click()
        return self

    def get_email_input(self):
        return self.driver.find_element(By.ID, "email")

    def get_password_input(self):
        return self.driver.find_element(By.ID, "password")

    def get_role_select(self):
        return self.driver.find_element(By.ID, "role")

    def get_first_name_input(self):
        return self.driver.find_element(By.ID, "first_name")

    def get_last_name_input(self):
        return self.driver.find_element(By.ID, "last_name")

    def get_phone_input(self):
        return self.driver.find_element(By.ID, "phone_number")

    def fill_email(self, email):
        input_field = self.get_email_input()
        input_field.clear()
        input_field.send_keys(email)
        return self

    def fill_password(self, password):
        input_field = self.get_password_input()
        input_field.clear()
        input_field.send_keys(password)
        return self

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

    def fill_phone(self, phone):
        input_field = self.get_phone_input()
        input_field.clear()
        input_field.send_keys(phone)
        return self

    def get_submit_button(self):
        return self.driver.find_element(
            By.XPATH, "//div[@class='modal-overlay']//button[@type='submit']"
        )

    def click_submit_button(self):
        self.get_submit_button().click()
        return self

    def get_confirm_delete_button(self):
        return self.driver.find_element(
            By.XPATH,
            "/html/body/div/div/main/div/div[3]/div/div[3]/button[2]",
        )

    def click_confirm_delete_button(self):
        self.get_confirm_delete_button().click()
        return self

    def get_success_alert(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert.alert-success"))
        )

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ManagerShipmentsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url="http://localhost:3000/manager-shipments"):
        self.driver.get(url)
        return self

    def get_table(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "courier-shipments-table"))
        )

    def get_all_rows(self):
        table = self.get_table()
        return table.find_elements(By.TAG_NAME, "tr")[1:]

    def click_details_button(self, row_index=0):
        rows = self.get_all_rows()
        details_btn = rows[row_index].find_element(By.CLASS_NAME, "btn-details")
        details_btn.click()
        return self

    def click_status_button(self, row_index=0):
        rows = self.get_all_rows()
        status_btn = rows[row_index].find_element(By.CLASS_NAME, "btn-status")
        status_btn.click()
        return self

    def click_assign_courier_button(self, row_index=0):
        rows = self.get_all_rows()
        assign_btn = rows[row_index].find_element(By.CLASS_NAME, "btn-assign")
        assign_btn.click()
        return self

    def get_modal_overlay(self):
        return self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-overlay"))
        )

    def get_modal_close_button(self):
        return self.driver.find_element(By.CLASS_NAME, "modal-close-btn")

    def get_status_select(self):
        return self.driver.find_element(By.CLASS_NAME, "status-select")

    def select_status(self, status_value):
        status_select = self.get_status_select()
        status_select.click()
        option = self.driver.find_element(
            By.CSS_SELECTOR, f"option[value='{status_value}']"
        )
        option.click()
        return self

    def get_submit_button(self):
        return self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    def get_cancel_button(self):
        return self.driver.find_element(By.CLASS_NAME, "btn-cancel")

    def get_filter_status(self):
        return self.driver.find_element(By.ID, "filter-status")

    def set_filter_status(self, status):
        filter_select = self.get_filter_status()
        filter_select.click()
        option = self.driver.find_element(
            By.CSS_SELECTOR, f"#filter-status option[value='{status}']"
        )
        option.click()
        return self

    def get_filter_sender(self):
        return self.driver.find_element(By.ID, "filter-sender")

    def set_filter_sender(self, sender_text):
        sender_input = self.get_filter_sender()
        sender_input.clear()
        sender_input.send_keys(sender_text)
        return self

    def get_refresh_button(self):
        return self.driver.find_element(By.CLASS_NAME, "refresh-btn")

    def get_clear_filters_button(self):
        return self.driver.find_element(By.CLASS_NAME, "clear-filters-btn")

    def get_status_from_row(self, row_index=0):
        rows = self.get_all_rows()
        status_badge = rows[row_index].find_element(By.CLASS_NAME, "table-status-badge")
        return status_badge.text

    def get_courier_select(self):
        return self.driver.find_element(By.ID, "courier-select")

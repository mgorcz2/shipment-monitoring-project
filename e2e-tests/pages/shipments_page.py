import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShipmentsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        self.shipment_cards = (By.CSS_SELECTOR, ".shipment-card")
        self.modal_overlay = (By.CSS_SELECTOR, ".modal-overlay")
        self.modal_details = (By.CSS_SELECTOR, ".shipment-details")
        self.modal_close_btn = (By.CSS_SELECTOR, ".modal-close-btn")
        self.role_filter_select = (By.ID, "role-filter")

    def open(self, base_url):
        self.driver.get(f"{base_url}/shipments")
        time.sleep(1)

    def get_shipments_count(self):
        shipments = self.driver.find_elements(*self.shipment_cards)
        return len(shipments)

    def has_shipments(self):
        return self.get_shipments_count() > 0

    def find_shipment_by_recipient_email(self, recipient_email):
        shipment_cards = self.driver.find_elements(*self.shipment_cards)
        for card in shipment_cards:
            card_text = card.text
            if recipient_email in card_text:
                return card
        return None

    def get_shipment_card_text(self, recipient_email):
        shipment_card = self.find_shipment_by_recipient_email(recipient_email)
        return shipment_card.text if shipment_card else None

    def click_details_button_for_shipment(self, recipient_email):
        shipment_card = self.find_shipment_by_recipient_email(recipient_email)
        details_button = shipment_card.find_element(By.TAG_NAME, "button")
        details_button.click()
        time.sleep(1)

    def get_details_modal(self, timeout=1):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.modal_overlay)
        )

    def get_modal_details_text(self):
        modal_content = self.driver.find_element(*self.modal_details)
        return modal_content.text

    def close_details_modal(self):
        close_button = self.driver.find_element(*self.modal_close_btn)
        close_button.click()
        time.sleep(1)

    def get_role_filter(self):
        return self.driver.find_element(*self.role_filter_select)

    def select_filter(self, filter_value):
        filter_element = self.get_role_filter()
        filter_element.click()
        option = filter_element.find_element(
            By.CSS_SELECTOR, f"option[value='{filter_value}']"
        )
        option.click()
        time.sleep(0.5)

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ShipmentsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
        self.shipments_container = (By.CSS_SELECTOR, ".shipments-container")
        self.shipment_cards = (By.CSS_SELECTOR, ".shipment-card")
        self.shipment_card_first = (By.CSS_SELECTOR, ".shipment-card:first-child")
        
    def open(self, base_url):
        self.driver.get(f"{base_url}/shipments")
        time.sleep(1)
    
    def get_shipments_count(self):
        shipments = self.driver.find_elements(*self.shipment_cards)
        return len(shipments)
    
    def has_shipments(self):
        return self.get_shipments_count() > 0
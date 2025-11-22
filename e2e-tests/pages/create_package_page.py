import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CreatePackagePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    origin_street = (By.ID, "origin-street-input")
    origin_street_number = (By.ID, "origin-street-number-input")
    origin_city = (By.ID, "origin-city-input")
    origin_postcode = (By.NAME, "origin_postcode")

    destination_street = (By.ID, "destination-street-input")
    destination_street_number = (By.ID, "destination-street-number-input")
    destination_city = (By.CSS_SELECTOR, "input[name='destination_city']")
    destination_postcode = (By.XPATH, "//*[@id=\"create-package-form\"]/input[8]")

    recipient_email = (By.ID, "recipient-email-input")

    weight = (By.XPATH, "//input[@name='weight']")
    length = (By.NAME, "length")
    width = (By.CSS_SELECTOR, "input[name='width']")
    height = (By.XPATH, "//*[@id=\"create-package-form\"]/input[13]")
    fragile_checkbox = (By.NAME, "fragile")

    submit_button = (By.ID, "submit-package-button")

    success_message = (By.CLASS_NAME, "create-package-success")
    error_message = (By.XPATH, "//div[@class='create-package-error']")

    geocoding_success = (By.XPATH, "//div[contains(@class, 'geocoding-status') and contains(@class, 'success')]")
    geocoding_error = (By.CSS_SELECTOR, ".geocoding-status.error")

    shipping_cost_total = (By.XPATH, "//div[@class='cost-row total']//span[@class='cost-value']")
    distance_value = (By.CLASS_NAME, "distance-value")

    def open(self, base_url):
        self.driver.get(f"{base_url}/create-shipment")
        time.sleep(1)

    def fill_origin_address(self, street, number, city, postcode):
        self.driver.find_element(*self.origin_street).send_keys(street)
        self.driver.find_element(*self.origin_street_number).send_keys(number)
        self.driver.find_element(*self.origin_city).send_keys(city)
        self.driver.find_element(*self.origin_postcode).send_keys(postcode)
        time.sleep(1)

    def fill_destination_address(self, street, number, city, postcode):
        self.driver.find_element(*self.destination_street).send_keys(street)
        self.driver.find_element(*self.destination_street_number).send_keys(number)
        self.driver.find_element(*self.destination_city).send_keys(city)
        self.driver.find_element(*self.destination_postcode).send_keys(postcode)
        time.sleep(1)

    def fill_recipient_email(self, email):
        self.driver.find_element(*self.recipient_email).send_keys(email)

    def fill_package_details(self, weight, length, width, height, fragile=False):
        self.driver.find_element(*self.weight).send_keys(str(weight))
        self.driver.find_element(*self.length).send_keys(str(length))
        self.driver.find_element(*self.width).send_keys(str(width))
        self.driver.find_element(*self.height).send_keys(str(height))

        if fragile:
            checkbox = self.driver.find_element(*self.fragile_checkbox)
            if not checkbox.is_selected():
                checkbox.click()

        time.sleep(1)

    def submit_package(self):
        button = self.driver.find_element(*self.submit_button)
        button.click()
        time.sleep(2)

    def wait_for_origin_geocoding(self, timeout=10):
        try:
            self.wait.until(EC.presence_of_element_located(self.geocoding_success))
            return True
        except:
            return False

    def wait_for_destination_geocoding(self, timeout=10):
        try:
            elements = self.wait.until(
                lambda driver: driver.find_elements(*self.geocoding_success)
            )
            return len(elements) >= 2
        except:
            return False

    def wait_for_both_geocoding(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: len(driver.find_elements(*self.geocoding_success)) >= 2
            )
            return True
        except:
            return False

    def create_full_package(self, origin, destination, recipient_email, package_data):
        self.fill_origin_address(
            origin["street"], origin["number"], origin["city"], origin["postcode"]
        )
        
        self.wait_for_origin_geocoding()

        self.fill_destination_address(
            destination["street"],
            destination["number"],
            destination["city"],
            destination["postcode"],
        )
        
        self.wait_for_destination_geocoding()

        self.fill_recipient_email(recipient_email)

        self.fill_package_details(
            package_data["weight"],
            package_data["length"],
            package_data["width"],
            package_data["height"],
            package_data.get("fragile", False),
        )
        
        time.sleep(2)

        self.submit_package()

    def is_origin_geocoded(self):
        try:
            elements = self.driver.find_elements(*self.geocoding_success)
            return len(elements) > 0
        except:
            return False

    def is_destination_geocoded(self):
        try:
            elements = self.driver.find_elements(*self.geocoding_success)
            return len(elements) >= 2
        except:
            return False

    def get_shipping_cost(self):
        try:
            cost_element = self.wait.until(
                EC.presence_of_element_located(self.shipping_cost_total)
            )
            return cost_element.text
        except:
            return None

    def get_distance(self):
        try:
            distance_element = self.wait.until(
                EC.presence_of_element_located(self.distance_value)
            )
            return distance_element.text
        except:
            return None

    def get_success_message(self):
        try:
            msg = self.wait.until(EC.presence_of_element_located(self.success_message))
            return msg.text
        except:
            return None

    def get_error_message(self):
        try:
            msg = self.driver.find_element(*self.error_message)
            return msg.text
        except:
            return None

    def is_submit_button_enabled(self):
        button = self.driver.find_element(*self.submit_button)
        return button.is_enabled()

import time
import uuid

import pytest
from conftest import register_client_via_api
from pages.create_package_page import CreatePackagePage
from pages.login_page import LoginPage
from pages.shipments_page import ShipmentsPage


def test_create_package(authenticated_driver):
    """Test creating a package and verifying it appears in shipments list"""
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Krakowska",
        "number": "1",
        "city": "Warszawa",
        "postcode": "00-001",
    }

    destination = {
        "street": "Marszałkowska",
        "number": "10",
        "city": "Warszawa",
        "postcode": "00-590",
    }

    package_data = {
        "weight": 5,
        "length": 30,
        "width": 20,
        "height": 10,
        "fragile": False,
    }

    recipient_email = "created_package_test@example.com"

    package_page.create_full_package(origin, destination, recipient_email, package_data)

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    shipments_page = ShipmentsPage(authenticated_driver)
    assert shipments_page.has_shipments()

    card_text = shipments_page.get_shipment_card_text(recipient_email)
    assert card_text is not None
    assert recipient_email in card_text
    assert "Warszawa" in card_text


def test_shipping_cost_calculation(authenticated_driver):
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    package_page.fill_origin_address("Krakowska", "1", "Warszawa", "00-001")
    package_page.wait_for_origin_geocoding()

    package_page.fill_destination_address("Marszałkowska", "10", "Warszawa", "00-590")
    package_page.wait_for_destination_geocoding()

    package_page.fill_recipient_email("test@test.com")

    package_page.fill_package_details(5, 30, 20, 10, fragile=False)
    time.sleep(3)

    cost = package_page.get_shipping_cost()
    assert cost is not None


def test_fragile_package_cost(authenticated_driver):
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    package_page.fill_origin_address("Krakowska", "1", "Warszawa", "00-001")
    package_page.wait_for_origin_geocoding()
    package_page.fill_destination_address("Marszałkowska", "10", "Warszawa", "00-590")
    package_page.wait_for_destination_geocoding()
    package_page.fill_recipient_email("test@test.com")
    package_page.fill_package_details(5, 30, 20, 10, fragile=False)
    time.sleep(3)

    cost_normal = package_page.get_shipping_cost()
    assert cost_normal is not None

    checkbox = authenticated_driver.find_element(*package_page.fragile_checkbox)
    checkbox.click()
    time.sleep(3)

    cost_fragile = package_page.get_shipping_cost()
    assert cost_fragile is not None
    assert cost_fragile > cost_normal


def test_package_appears_in_shipments_list(authenticated_driver):
    """Test that created fragile package appears in shipments list with correct details"""
    package_page = CreatePackagePage(authenticated_driver)
    shipments_page = ShipmentsPage(authenticated_driver)

    origin = {
        "street": "Krakowska",
        "number": "1",
        "city": "Warszawa",
        "postcode": "00-001",
    }

    destination = {
        "street": "Marszałkowska",
        "number": "10",
        "city": "Warszawa",
        "postcode": "00-590",
    }

    package_data = {
        "weight": 3,
        "length": 25,
        "width": 15,
        "height": 8,
        "fragile": True,
    }

    recipient_email = "fragile_package_test@example.com"

    package_page.open("http://localhost:3000")
    package_page.create_full_package(origin, destination, recipient_email, package_data)

    time.sleep(5)

    assert "/shipments" in authenticated_driver.current_url
    assert shipments_page.has_shipments()

    card_text = shipments_page.get_shipment_card_text(recipient_email)
    assert card_text is not None
    assert recipient_email in card_text
    assert "Warszawa" in card_text


def test_recipient_sees_shipment_assigned_to_them(driver, authenticated_driver):
    """Test that sender creates package for recipient, then recipient logs in and sees the shipment"""
    recipient_unique_id = str(uuid.uuid4())[:8]
    recipient_user_data = {
        "email": f"recipient_{recipient_unique_id}@test.com",
        "password": "TestPassword123!",
        "role": "client",
    }
    recipient_client_data = {
        "first_name": "Recipient",
        "last_name": "User",
        "phone_number": "444555666",
        "address": "Recipient Street 2",
    }

    recipient = register_client_via_api(recipient_user_data, recipient_client_data)
    assert recipient is not None

    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Krakowska",
        "number": "5",
        "city": "Kraków",
        "postcode": "30-001",
    }

    destination = {
        "street": "Główna",
        "number": "15",
        "city": "Gdańsk",
        "postcode": "80-001",
    }

    package_data = {
        "weight": 2,
        "length": 20,
        "width": 15,
        "height": 10,
        "fragile": False,
    }

    package_page.create_full_package(
        origin, destination, recipient_user_data["email"], package_data
    )

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    driver.execute_script("localStorage.clear();")

    login_page = LoginPage(driver)
    login_page.open("http://localhost:3000")
    login_page.login_attempt(
        recipient_user_data["email"], recipient_user_data["password"]
    )

    time.sleep(3)
    recipient_token = driver.execute_script("return localStorage.getItem('token');")
    assert recipient_token is not None

    shipments_page = ShipmentsPage(driver)
    shipments_page.open("http://localhost:3000")

    time.sleep(3)

    assert shipments_page.has_shipments()

    card_text = shipments_page.get_shipment_card_text(recipient_user_data["email"])
    assert card_text is not None
    assert recipient_user_data["email"] in card_text
    assert "Kraków" in card_text
    assert "Gdańsk" in card_text

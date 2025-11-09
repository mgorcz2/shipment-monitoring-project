import time

import pytest
from pages.create_package_page import CreatePackagePage


def test_create_package_full_flow(authenticated_driver):
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

    package_page.create_full_package(
        origin, destination, "odbiorca@test.com", package_data
    )

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url


def test_shipping_cost_calculation(authenticated_driver):
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    package_page.fill_origin_address("Krakowska", "1", "Warszawa", "00-001")
    time.sleep(2)

    package_page.fill_destination_address("Marszałkowska", "10", "Warszawa", "00-590")
    time.sleep(2)

    package_page.fill_recipient_email("test@test.com")

    package_page.fill_package_details(5, 30, 20, 10, fragile=False)
    time.sleep(2)

    cost = package_page.get_shipping_cost()
    assert cost is not None


def test_fragile_package_increases_cost(authenticated_driver):
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    package_page.fill_origin_address("Krakowska", "1", "Warszawa", "00-001")
    time.sleep(2)
    package_page.fill_destination_address("Marszałkowska", "10", "Warszawa", "00-590")
    time.sleep(2)
    package_page.fill_recipient_email("test@test.com")
    package_page.fill_package_details(5, 30, 20, 10, fragile=False)
    time.sleep(2)

    cost_normal = package_page.get_shipping_cost()

    checkbox = authenticated_driver.find_element(*package_page.fragile_checkbox)
    checkbox.click()
    time.sleep(2)

    cost_fragile = package_page.get_shipping_cost()

    assert cost_fragile > cost_normal

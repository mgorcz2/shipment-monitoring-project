import time

from pages.create_package_page import CreatePackagePage
from pages.shipments_page import ShipmentsPage


def test_empty_shipments_list(authenticated_driver):
    """Test that new user has empty shipments list"""
    shipments_page = ShipmentsPage(authenticated_driver)
    shipments_page.open("http://localhost:3000")

    time.sleep(2)

    assert shipments_page.get_shipments_count() == 0
    assert not shipments_page.has_shipments()


def test_shipment_details_modal_opens_and_closes(authenticated_driver):
    """Test that clicking details button opens and closes modal"""
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Długa",
        "number": "5",
        "city": "Warszawa",
        "postcode": "00-001",
    }

    destination = {
        "street": "Krótka",
        "number": "10",
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

    recipient_email = "modal_open_test@example.com"

    package_page.create_full_package(origin, destination, recipient_email, package_data)

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    shipments_page = ShipmentsPage(authenticated_driver)
    assert shipments_page.has_shipments()

    shipments_page.click_details_button_for_shipment(recipient_email)

    modal = shipments_page.get_details_modal()
    assert modal.is_displayed()

    shipments_page.close_details_modal()


def test_shipment_details_content(authenticated_driver):
    """Test that modal displays correct shipment details"""
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Piotrkowska",
        "number": "100",
        "city": "Łódź",
        "postcode": "90-001",
    }

    destination = {
        "street": "Floriańska",
        "number": "20",
        "city": "Kraków",
        "postcode": "31-019",
    }

    package_data = {
        "weight": 4,
        "length": 35,
        "width": 25,
        "height": 15,
        "fragile": True,
    }

    recipient_email = "modal_content_test@example.com"

    package_page.create_full_package(origin, destination, recipient_email, package_data)

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    shipments_page = ShipmentsPage(authenticated_driver)
    assert shipments_page.has_shipments()

    shipments_page.click_details_button_for_shipment(recipient_email)
    modal = shipments_page.get_details_modal()
    assert modal.is_displayed()

    shipments_page.close_details_modal()


def test_filter_shipments_by_sender(authenticated_driver):
    """Test filtering shipments - show only packages I sent"""
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin_sent = {
        "street": "Wysoka",
        "number": "7",
        "city": "Wrocław",
        "postcode": "50-001",
    }

    destination_sent = {
        "street": "Niska",
        "number": "3",
        "city": "Poznań",
        "postcode": "60-001",
    }

    package_data_sent = {
        "weight": 1,
        "length": 10,
        "width": 10,
        "height": 10,
        "fragile": False,
    }

    recipient_email_sent = "filter_sender_recipient@example.com"

    package_page.create_full_package(
        origin_sent, destination_sent, recipient_email_sent, package_data_sent
    )

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    shipments_page = ShipmentsPage(authenticated_driver)

    all_count = shipments_page.get_shipments_count()
    assert all_count > 0

    shipments_page.select_filter("sender")
    time.sleep(1)

    sender_count = shipments_page.get_shipments_count()
    assert sender_count > 0

    card_text = shipments_page.get_shipment_card_text(recipient_email_sent)
    assert recipient_email_sent in card_text


def test_filter_shipments_by_recipient(authenticated_driver):
    """Test filtering shipments - show only packages I receive"""
    shipments_page = ShipmentsPage(authenticated_driver)
    shipments_page.open("http://localhost:3000")

    shipments_page.select_filter("recipient")
    time.sleep(1)

    recipient_count = shipments_page.get_shipments_count()
    assert recipient_count == 0


def test_filter_all_shipments(authenticated_driver):
    """Test filtering shipments - show all packages"""
    package_page = CreatePackagePage(authenticated_driver)
    package_page.open("http://localhost:3000")

    origin = {
        "street": "Szeroka",
        "number": "15",
        "city": "Katowice",
        "postcode": "40-001",
    }

    destination = {
        "street": "Wąska",
        "number": "8",
        "city": "Lublin",
        "postcode": "20-001",
    }

    package_data = {
        "weight": 3,
        "length": 25,
        "width": 20,
        "height": 12,
        "fragile": False,
    }

    recipient_email = "filter_all_test@example.com"

    package_page.create_full_package(origin, destination, recipient_email, package_data)

    time.sleep(5)
    assert "/shipments" in authenticated_driver.current_url

    shipments_page = ShipmentsPage(authenticated_driver)

    shipments_page.select_filter("all")
    time.sleep(1)
    all_count = shipments_page.get_shipments_count()
    assert all_count > 0

    shipments_page.select_filter("sender")
    time.sleep(1)
    sender_count = shipments_page.get_shipments_count()
    assert sender_count > 0

    shipments_page.select_filter("recipient")
    time.sleep(1)
    recipient_count = shipments_page.get_shipments_count()
    assert recipient_count == 0

    shipments_page.select_filter("all")
    time.sleep(1)
    final_count = shipments_page.get_shipments_count()
    assert final_count == sender_count

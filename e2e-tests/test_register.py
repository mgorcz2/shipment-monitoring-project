import time

from conftest import create_user_via_api
from pages.register_page import RegisterPage

FRONTEND_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"


def test_successful_registration(driver, sample_registration_data):
    """Test successful user registration"""
    test_data = sample_registration_data
    register_page = RegisterPage(driver)
    register_page.open(FRONTEND_URL)

    register_page.register_attempt(
        test_data["email"],
        test_data["password"],
        test_data["first_name"],
        test_data["last_name"],
        test_data["phone"],
        test_data["address"],
    )

    success_element = register_page.get_success_element(timeout=10)
    assert success_element is not None
    assert success_element.is_displayed()

    success_text = success_element.text
    assert success_text is not None
    assert len(success_text) > 0
    assert "sukcesem" in success_text or "success" in success_text.lower()

    time.sleep(3)
    assert "/login" in driver.current_url or "/shipments" in driver.current_url


def test_registration_with_existing_email(driver, sample_registration_data):
    """Test registration with already existing email"""
    existing_email = sample_registration_data["email"]

    sample_registration_data["email"] = existing_email
    create_user_via_api(sample_registration_data)

    register_page = RegisterPage(driver)
    register_page.open(FRONTEND_URL)

    register_page.register_attempt(
        existing_email,
        "Password123!",
        "Another",
        "User",
        "987654321",
        "Another Street 456",
    )

    error_element = register_page.get_error_element(timeout=5)
    assert error_element is not None
    assert error_element.is_displayed()

    error_text = error_element.text
    assert error_text is not None
    assert len(error_text) > 0
    assert "already registered" in error_text.lower()


def test_registration_with_invalid_data(driver):
    """Test registration with invalid data"""
    register_page = RegisterPage(driver)
    register_page.open(FRONTEND_URL)

    register_page.register_attempt(
        "mail@example.com", "string123", "aaa", "ss", "abc", "aaa"
    )

    error_element = register_page.get_error_element(timeout=5)
    assert error_element is not None
    assert error_element.is_displayed()

    error_text = error_element.text
    assert error_text is not None
    assert "invalid" in error_text.lower() or "error" in error_text.lower()

import time

from pages.profile_page import ProfilePage


def test_client_views_profile_page(authenticated_driver):
    driver = authenticated_driver
    profile_page = ProfilePage(driver)

    profile_page.open()
    time.sleep(2)

    assert profile_page.get_edit_button() is not None


def test_client_updates_profile(authenticated_driver):
    driver = authenticated_driver
    profile_page = ProfilePage(driver)

    profile_page.open()
    time.sleep(2)

    profile_page.click_edit_button()
    time.sleep(1)

    new_first_name = "Marcin"
    new_last_name = "Testowy"
    new_phone = "987654321"

    profile_page.fill_first_name(new_first_name)
    profile_page.fill_last_name(new_last_name)
    profile_page.fill_phone_number(new_phone)

    profile_page.click_save_button()
    time.sleep(2)

    assert profile_page.get_success_alert() is not None

    driver.refresh()
    time.sleep(2)

    assert profile_page.get_first_name_value() == new_first_name
    assert profile_page.get_last_name_value() == new_last_name
    assert profile_page.get_phone_value() == new_phone


def test_client_deletes_account(authenticated_driver):
    driver = authenticated_driver
    profile_page = ProfilePage(driver)

    profile_page.open()
    time.sleep(2)

    profile_page.click_delete_account_button()
    time.sleep(1)

    confirm_button = profile_page.get_delete_confirm_button()
    confirm_button.click()
    time.sleep(3)

    assert "login" in driver.current_url

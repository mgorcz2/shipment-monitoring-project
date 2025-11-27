import time
import uuid

from pages.admin_panel_page import AdminPanelPage


def test_admin_views_users_table(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    assert admin_panel.get_user_table() is not None
    assert len(admin_panel.get_all_table_rows()) > 0


def test_admin_filters_users_by_role(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    total_rows = len(admin_panel.get_all_table_rows())

    admin_panel.set_role_filter("client")
    time.sleep(1)

    filtered_rows = len(admin_panel.get_all_table_rows())
    assert filtered_rows <= total_rows


def test_admin_views_user_details(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    admin_panel.click_details_button(0)
    time.sleep(1)

    assert admin_panel.get_modal_overlay() is not None
    assert admin_panel.get_modal_close_button() is not None

    admin_panel.click_modal_close_button()
    time.sleep(1)


def test_admin_edits_user_and_saves(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    admin_panel.click_edit_button(0)
    time.sleep(1)

    assert admin_panel.get_modal_overlay() is not None

    new_first_name = "Edited"
    admin_panel.fill_first_name(new_first_name)

    admin_panel.click_submit_button()
    time.sleep(2)

    assert admin_panel.get_success_alert() is not None


def test_admin_deletes_user(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    initial_count = len(admin_panel.get_all_table_rows())

    admin_panel.click_delete_button(0)
    time.sleep(1)

    assert admin_panel.get_modal_overlay() is not None

    admin_panel.click_confirm_delete_button()
    time.sleep(2)

    assert admin_panel.get_success_alert() is not None

    new_count = len(admin_panel.get_all_table_rows())
    assert new_count < initial_count


def test_admin_registers_new_staff(authenticated_admin_driver):
    driver = authenticated_admin_driver
    admin_panel = AdminPanelPage(driver)
    admin_panel.open()
    time.sleep(2)

    initial_count = len(admin_panel.get_all_table_rows())

    admin_panel.click_register_staff_button()
    time.sleep(1)

    assert admin_panel.get_modal_overlay() is not None

    unique_id = str(uuid.uuid4())[:8]
    admin_panel.fill_email(f"staff_{unique_id}@test.com")
    admin_panel.fill_password("Test1234!")
    admin_panel.fill_first_name("Test")
    admin_panel.fill_last_name("Staff")
    admin_panel.fill_phone("123456789")

    admin_panel.click_submit_button()
    time.sleep(3)

    new_count = len(admin_panel.get_all_table_rows())
    assert new_count > initial_count

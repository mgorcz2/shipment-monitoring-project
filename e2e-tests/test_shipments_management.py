import time

from pages.manager_shipments_page import ManagerShipmentsPage


def test_manager_can_view_shipments_page(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    assert manager_page.get_table() is not None


def test_manager_can_view_shipment_details(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    manager_page.click_details_button(0)
    time.sleep(1)

    assert manager_page.get_modal_overlay().is_displayed()

    manager_page.get_modal_close_button().click()
    time.sleep(1)


def test_manager_can_open_status_change_modal(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    manager_page.click_status_button(0)
    time.sleep(1)

    assert manager_page.get_status_select() is not None

    manager_page.get_cancel_button().click()
    time.sleep(1)


def test_manager_can_change_shipment_status(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    rows = manager_page.get_all_rows()
    assert len(rows) > 0

    manager_page.click_status_button(0)
    time.sleep(1)

    manager_page.select_status("delivered")
    time.sleep(0.5)

    manager_page.get_submit_button().click()
    time.sleep(3)

    new_status = manager_page.get_status_from_row(0)
    assert "Dostarczona" in new_status


def test_manager_can_use_status_filter(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    rows = manager_page.get_all_rows()
    total_count = len(rows)

    manager_page.set_filter_status("delivered")
    time.sleep(1)

    filtered_rows = manager_page.get_all_rows()
    assert len(filtered_rows) <= total_count

    manager_page.get_clear_filters_button().click()
    time.sleep(1)

    reset_rows = manager_page.get_all_rows()
    assert len(reset_rows) == total_count


def test_manager_can_use_sender_filter(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    rows = manager_page.get_all_rows()
    total_count = len(rows)

    manager_page.set_filter_sender("test")
    time.sleep(1)

    filtered_rows = manager_page.get_all_rows()
    assert len(filtered_rows) <= total_count

    manager_page.get_clear_filters_button().click()
    time.sleep(1)


def test_manager_can_refresh_shipments_list(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    initial_rows = manager_page.get_all_rows()
    initial_count = len(initial_rows)

    manager_page.get_refresh_button().click()
    time.sleep(2)

    assert manager_page.get_table() is not None

    refreshed_rows = manager_page.get_all_rows()
    assert len(refreshed_rows) == initial_count


def test_manager_can_open_assign_courier_modal(manager_with_package):
    driver = manager_with_package
    manager_page = ManagerShipmentsPage(driver)

    manager_page.open()
    time.sleep(2)

    manager_page.click_assign_courier_button(0)
    time.sleep(1)

    assert manager_page.get_courier_select() is not None

    manager_page.get_modal_close_button().click()
    time.sleep(1)

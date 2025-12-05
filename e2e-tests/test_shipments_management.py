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

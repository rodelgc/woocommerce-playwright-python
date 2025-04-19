from typing import Dict
from playwright.sync_api import Page

from tests._models.customer.my_account_dashboard_page import MyAccountDashboardPage
from tests._models.customer.my_account_details_page import MyAccountDetailsPage
from tests._models.customer.my_account_login_page import MyAccountLoginPage


def test_guest_can_register(page: Page, customer_registration_data: Dict[str, any]):
    # Customer data
    customer_username = customer_registration_data["username"]
    customer_email = customer_registration_data["email"]
    customer_first_name = customer_registration_data["first_name"]
    customer_last_name = customer_registration_data["last_name"]
    customer_password = customer_registration_data["password"]

    def goto_my_account_page_and_register() -> MyAccountDashboardPage:
        page.goto("my-account")
        my_account_login_page = MyAccountLoginPage(page)
        my_dashboard_page = my_account_login_page.register(
            customer_email, customer_password
        )

        return my_dashboard_page

    def verify_dashboard_page_details(dashboard_page: MyAccountDashboardPage) -> None:
        dashboard_page.expect_greeting_to_contain(customer_username)

    def goto_account_details_page_and_update_first_last_names():
        page.goto("my-account/edit-account")
        my_details_page = MyAccountDetailsPage(page)
        my_details_page.expect_display_name_textbox_to_have_value(customer_username)
        my_details_page.expect_email_address_textbox_to_have_value(customer_email)
        my_details_page.update_details(
            {"first_name": customer_first_name, "last_name": customer_last_name}
        )

    dashboard_page = goto_my_account_page_and_register()
    verify_dashboard_page_details(dashboard_page)
    goto_account_details_page_and_update_first_last_names()

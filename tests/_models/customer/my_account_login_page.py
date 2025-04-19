import re
from playwright.sync_api import Page, expect

from tests._models.customer.my_account_dashboard_page import MyAccountDashboardPage


class MyAccountLoginPage:

    def __init__(self, page: Page):
        self.page = page

        expect(self.page).to_have_url(re.compile(r".*/my-account"))
        expect(self.page).to_have_title(re.compile(r"^My account .*"))

    def register(self, email: str, password: str):
        # Locators
        email_textbox = self.page.get_by_role(
            "textbox", name="Email address Required", exact=True
        )
        password_textbox = self.page.locator("#reg_password")
        strong_password_indicator = self.page.get_by_text("Strong")
        register_button = self.page.get_by_role("button", name="Register")

        # Actions
        email_textbox.press_sequentially(email)
        password_textbox.press_sequentially(password)
        expect(strong_password_indicator).to_be_visible()
        register_button.click()

        return MyAccountDashboardPage(self.page)

import re
from typing import Dict
from playwright.sync_api import Page, expect


class MyAccountDetailsPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        expect(self.page).to_have_url(re.compile(r"^.*/my-account/edit-account"))
        expect(self.page).to_have_title(re.compile(r"^Account details"))
        expect(self.page.get_by_role("heading", name="Account details")).to_be_visible()

    def expect_display_name_textbox_to_have_value(
        self, expected_display_name: str
    ) -> None:
        display_name_textbox = self.page.get_by_role("textbox", name="Display name")
        expect(display_name_textbox).to_have_value(expected_display_name)

    def expect_email_address_textbox_to_have_value(self, expected_email: str) -> None:
        email_address_textbox = self.page.get_by_role("textbox", name="Email address")
        expect(email_address_textbox).to_have_value(expected_email)

    def update_details(self, new_details: Dict[str, any]) -> None:
        # New data
        new_first_name = new_details["first_name"]
        new_last_name = new_details["last_name"]

        # Locators
        first_name_textbox = self.page.get_by_role("textbox", name="First name")
        last_name_textbox = self.page.get_by_role("textbox", name="Last name")
        save_changes_button = self.page.get_by_role("button", name="Save changes")
        success_message = self.page.get_by_text("Account details changed")

        # Actions
        first_name_textbox.fill(new_first_name)
        last_name_textbox.fill(new_last_name)
        save_changes_button.click()
        expect(success_message).to_be_visible()

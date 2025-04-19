import re
from playwright.sync_api import Page, expect


class MyAccountDashboardPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        expect(self.page).to_have_url(re.compile(r"^.*/my-account/?$"))
        expect(self.page).to_have_title(re.compile(r"^My account"))
        expect(self.page.get_by_role("heading", name="My account")).to_be_visible()
        expect(
            self.page.get_by_label("Account pages").get_by_role("link", name="Log out")
        ).to_be_visible()

    def expect_greeting_to_contain(self, display_name: str) -> None:
        greeting = self.page.get_by_text("Hello")
        expect(greeting).to_contain_text(display_name)

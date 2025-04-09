import re
import pytest
from playwright.sync_api import Page, expect

ADMIN_USERNAME = "user"
ADMIN_PASSWORD = "bitnami"


@pytest.fixture(scope="function", autouse=True)
def admin_login(page: Page):
    page.goto("http://localhost:8080/wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(ADMIN_USERNAME)
    page.get_by_label("Password", exact=True).fill(ADMIN_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page).to_have_title(re.compile("^Dashboard .* WordPress$"))
    expect(page.get_by_text(f"Howdy, {ADMIN_USERNAME}")).to_be_visible()

    yield


def test_install_woo(page: Page):
    page.goto("http://localhost:8080/wp-admin/plugin-install.php")
    expect(page).to_have_title(re.compile("^Add Plugins"))
    page.get_by_label("Search Plugins", exact=True).fill("woocommerce")
    page.locator('[data-slug="woocommerce"]').click()
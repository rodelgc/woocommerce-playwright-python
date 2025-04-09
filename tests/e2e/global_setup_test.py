import re
import pytest
from playwright.sync_api import Page, expect
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")


@pytest.fixture(scope="function", autouse=True)
def admin_login(page: Page):
    page.goto("http://localhost:8080/wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()

    yield


def test_woo_home(page: Page):
    page.goto("http://localhost:8080/wp-admin/admin.php?page=wc-admin")
    expect(page).to_have_title("Home ‹ WooCommerce ‹ Reading Glow Co. — WooCommerce")

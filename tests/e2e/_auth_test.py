import re
import os
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_CUSTOMER_USERNAME = os.getenv("WORDPRESS_CUSTOMER_USERNAME")
WORDPRESS_CUSTOMER_PASSWORD = os.getenv("WORDPRESS_CUSTOMER_PASSWORD")


def test_auth_merchant(page: Page):
    page.goto("wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()

    # Save storage state into the file.
    page.context.storage_state(path="playwright/.auth/merchant.state.json")


def test_auth_customer(page: Page):
    page.goto("my-account")
    page.get_by_label("Username or email address").fill(WORDPRESS_CUSTOMER_USERNAME)
    page.get_by_role("textbox", name="Password Required").fill(
        WORDPRESS_CUSTOMER_PASSWORD
    )
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_role("heading", name="My account")).to_be_visible()
    expect(page.get_by_text(f"Hello {WORDPRESS_CUSTOMER_USERNAME}")).to_be_visible()

    page.context.storage_state(path="playwright/.auth/customer.state.json")

import re
import os
import pytest
from playwright.sync_api import Browser, BrowserContext, expect
from dotenv import load_dotenv

# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_CUSTOMER_USERNAME = os.getenv("WORDPRESS_CUSTOMER_USERNAME")
WORDPRESS_CUSTOMER_PASSWORD = os.getenv("WORDPRESS_CUSTOMER_PASSWORD")

# Storage state paths
MERCHANT_STORAGE_STATE_PATH = "playwright/.auth/merchant.state.json"
CUSTOMER_STORAGE_STATE_PATH = "playwright/.auth/customer.state.json"


@pytest.fixture(autouse=True, scope="session")
def merchant_login(browser: Browser, base_url: str):
    # Setup: log in as merchant and save storage state
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()
    merchant_storage_state = context.storage_state(path=MERCHANT_STORAGE_STATE_PATH)
    merchant_context = browser.new_context(
        base_url=base_url, storage_state=merchant_storage_state
    )

    yield merchant_context

    # Teardown: close all created contexts
    merchant_context.close()
    context.close()


@pytest.fixture(autouse=True, scope="session")
def customer_login(browser: Browser, base_url: str):
    # Setup: log in as customer and save storage state
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("my-account")
    page.get_by_label("Username or email address").fill(WORDPRESS_CUSTOMER_USERNAME)
    page.get_by_role("textbox", name="Password Required").fill(
        WORDPRESS_CUSTOMER_PASSWORD
    )
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_role("heading", name="My account")).to_be_visible()
    expect(page.get_by_text(f"Hello {WORDPRESS_CUSTOMER_USERNAME}")).to_be_visible()
    customer_storage_state = context.storage_state(path=CUSTOMER_STORAGE_STATE_PATH)
    customer_context = browser.new_context(
        base_url=base_url, storage_state=customer_storage_state
    )

    yield customer_context

    # Teardown: close all created contexts
    customer_context.close()
    context.close()


@pytest.fixture(scope="function")
def merchant_page(merchant_login: BrowserContext):
    return merchant_login.new_page()


@pytest.fixture(scope="function")
def customer_page(customer_login: BrowserContext):
    return customer_login.new_page()

import re
import os
import pytest
from playwright.sync_api import Browser, expect, StorageState
from dotenv import load_dotenv


# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_CUSTOMER_USERNAME = os.getenv("WORDPRESS_CUSTOMER_USERNAME")
WORDPRESS_CUSTOMER_PASSWORD = os.getenv("WORDPRESS_CUSTOMER_PASSWORD")


@pytest.fixture(autouse=True, scope="session")
def merchant_storage_state(browser: Browser, base_url: str):
    # Setup: log in as merchant and save storage state
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()
    merchant_storage_state = context.storage_state(
        path="playwright/.auth/merchant.state.json"
    )

    yield merchant_storage_state

    # Teardown: close unauthenticated context
    context.close()


@pytest.fixture(autouse=True, scope="session")
def customer_storage_state(browser: Browser, base_url: str):
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
    customer_storage_state = context.storage_state(
        path="playwright/.auth/customer.state.json"
    )

    yield customer_storage_state

    # Teardown: close unauthenticated context
    context.close()


@pytest.fixture(scope="function")
def merchant_page(
    merchant_storage_state: StorageState, browser: Browser, base_url: str
):
    # Setup: create authenticated merchant context
    merchant_context = browser.new_context(
        base_url=base_url,
        storage_state=merchant_storage_state,
    )
    merchant_page = merchant_context.new_page()

    yield merchant_page

    # Teardown: close authenticated context
    merchant_context.close()


@pytest.fixture(scope="function")
def customer_page(
    customer_storage_state: StorageState, browser: Browser, base_url: str
):
    # Setup: create authenticated customer context
    customer_context = browser.new_context(
        base_url=base_url,
        storage_state=customer_storage_state,
    )
    customer_page = customer_context.new_page()

    yield customer_page

    # Teardown: close authenticated context
    customer_context.close()

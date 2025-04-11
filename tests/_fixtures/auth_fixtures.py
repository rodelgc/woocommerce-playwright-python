# pylint: disable=redefined-outer-name

import os
import re
from typing import Tuple

import pytest
from dotenv import load_dotenv

from playwright.sync_api import Browser, StorageState, expect, BrowserContext

# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_CUSTOMER_USERNAME = os.getenv("WORDPRESS_CUSTOMER_USERNAME")
WORDPRESS_CUSTOMER_PASSWORD = os.getenv("WORDPRESS_CUSTOMER_PASSWORD")


def set_up_merchant_storage_state(browser: Browser, base_url: str) -> StorageState:
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()
    storage_state = context.storage_state(path="playwright/.auth/merchant.state.json")
    context.close()
    return storage_state


def set_up_customer_storage_state(browser: Browser, base_url: str) -> StorageState:
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
    storage_state = context.storage_state(path="playwright/.auth/customer.state.json")
    context.close()
    return storage_state


@pytest.fixture(autouse=True, scope="session")
def session_context(browser: Browser, base_url: str):
    merchant_storage_state = set_up_merchant_storage_state(browser, base_url)
    customer_storage_state = set_up_customer_storage_state(browser, base_url)

    yield merchant_storage_state, customer_storage_state


@pytest.fixture(scope="function")
def merchant_page(
    session_context: Tuple[StorageState, StorageState], browser: Browser, base_url: str
):
    merchant_storage_state, _ = session_context

    # Set up authenticated merchant context
    merchant_context = browser.new_context(
        base_url=base_url,
        storage_state=merchant_storage_state,
    )
    page = merchant_context.new_page()

    yield page

    # Teardown: close authenticated context
    merchant_context.close()


@pytest.fixture(scope="function")
def customer_page(
    session_context: Tuple[StorageState, StorageState], browser: Browser, base_url: str
):
    _, customer_storage_state = session_context

    # Setup: create authenticated customer context
    customer_context = browser.new_context(
        base_url=base_url,
        storage_state=customer_storage_state,
    )
    page = customer_context.new_page()

    yield page

    # Teardown: close authenticated context
    customer_context.close()

# pylint: disable=redefined-outer-name

import os
import re
from typing import Tuple
from datetime import datetime

import pytest
from pytest import FixtureRequest
from dotenv import load_dotenv

from playwright.sync_api import Browser, StorageState, expect

# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WORDPRESS_CUSTOMER_USERNAME = os.getenv("WORDPRESS_CUSTOMER_USERNAME")
WORDPRESS_CUSTOMER_PASSWORD = os.getenv("WORDPRESS_CUSTOMER_PASSWORD")

# Set paths
TEST_RESULTS_DIR = "playwright/test-results"
TRACES_HOME = f"{TEST_RESULTS_DIR}/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
AUTH_DIR = "playwright/.auth"


def set_up_traces_home() -> None:
    if not os.path.exists(TRACES_HOME):
        os.makedirs(TRACES_HOME)


def set_up_merchant_storage_state(browser: Browser, base_url: str) -> StorageState:
    context = browser.new_context(base_url=base_url)
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    page = context.new_page()
    page.goto("wp-admin")
    expect(page).to_have_title(re.compile("^Log In"))
    page.get_by_label("Username or Email Address").fill(WORDPRESS_USERNAME)
    page.get_by_label("Password", exact=True).fill(WORDPRESS_PASSWORD)
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_role("menuitem", name="Howdy")).to_be_visible()
    storage_state = context.storage_state(path=f"{AUTH_DIR}/merchant.state.json")
    context.tracing.stop(
        path=f"{TRACES_HOME}/_auth__set_up_merchant_storage_state.trace.zip",
    )
    context.close()
    return storage_state


def set_up_customer_storage_state(browser: Browser, base_url: str) -> StorageState:
    context = browser.new_context(base_url=base_url)
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    page = context.new_page()
    page.goto("my-account")
    page.get_by_label("Username or email address").fill(WORDPRESS_CUSTOMER_USERNAME)
    page.get_by_role("textbox", name="Password Required").fill(
        WORDPRESS_CUSTOMER_PASSWORD
    )
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_role("heading", name="My account")).to_be_visible()
    expect(page.get_by_text(f"Hello {WORDPRESS_CUSTOMER_USERNAME}")).to_be_visible()
    storage_state = context.storage_state(path=f"{AUTH_DIR}/customer.state.json")
    context.tracing.stop(
        path=f"{TRACES_HOME}/_auth__set_up_customer_storage_state.trace.zip",
    )
    context.close()
    return storage_state


def set_trace_path(suffix: str, request: FixtureRequest) -> str:
    module_name = request.module.__name__
    test_name = request.node.name
    trace_path = f"{TRACES_HOME}/{module_name}__{test_name}__{suffix}.trace.zip"
    return trace_path


@pytest.fixture(autouse=True, scope="session")
def session_context(browser: Browser, base_url: str):
    set_up_traces_home()
    merchant_storage_state = set_up_merchant_storage_state(browser, base_url)
    customer_storage_state = set_up_customer_storage_state(browser, base_url)

    yield merchant_storage_state, customer_storage_state


@pytest.fixture(scope="function")
def merchant_page(
    session_context: Tuple[StorageState, StorageState],
    browser: Browser,
    base_url: str,
    request: FixtureRequest,
):
    merchant_storage_state, _ = session_context
    trace_path = set_trace_path("merchant_context", request)

    # Set up authenticated merchant context
    merchant_context = browser.new_context(
        base_url=base_url,
        storage_state=merchant_storage_state,
    )
    merchant_context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    page = merchant_context.new_page()

    yield page

    # Teardown: close authenticated context
    merchant_context.tracing.stop(
        path=trace_path,
    )
    merchant_context.close()


@pytest.fixture(scope="function")
def customer_page(
    session_context: Tuple[StorageState, StorageState],
    browser: Browser,
    base_url: str,
    request: FixtureRequest,
):
    _, customer_storage_state = session_context
    trace_path = set_trace_path("customer_context", request)

    # Setup: create authenticated customer context
    customer_context = browser.new_context(
        base_url=base_url,
        storage_state=customer_storage_state,
    )
    customer_context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )
    page = customer_context.new_page()

    yield page

    # Teardown: close authenticated context
    customer_context.tracing.stop(
        path=trace_path,
    )
    customer_context.close()

import os
import pytest
from playwright.sync_api import Playwright
from dotenv import load_dotenv
from base64 import b64encode


# Load environment variables
load_dotenv("local.env")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")


@pytest.fixture(scope="session", autouse=True)
def request_context(playwright: Playwright, base_url: str):
    # Setup: create a request context
    auth_encoded = str(
        b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}".encode("utf-8")), "utf-8"
    )
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "accept": "application/json",
    }
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers=headers,
    )
    response = request_context.get("wp-json/wc/v3/", data={"_fields": "namespace"})
    assert response.ok
    assert response.json()["namespace"] == "wc/v3"

    yield request_context

    # Teardown: close the request context
    request_context.dispose()

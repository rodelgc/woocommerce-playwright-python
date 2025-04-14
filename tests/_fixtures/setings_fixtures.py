import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="session")
def settings_payment(request_context: APIRequestContext):
    """
    Enable BACS payment gateway.
    """
    path = "wp-json/wc/v3/payment_gateways/cod"
    data = {"enabled": True}

    response = request_context.put(path, data=data)
    assert response.ok
    is_enabled = response.json()["enabled"]
    assert is_enabled

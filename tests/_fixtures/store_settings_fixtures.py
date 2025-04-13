import pytest

from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="session", autouse=True)
def reset_merchant_settings(request_context: APIRequestContext):
    path = "wp-json/wp/v2/users/me?_locale=user"

    response = request_context.put(
        path, data={"woocommerce_meta": {"variable_product_tour_shown": "yes"}}
    )
    assert response.ok

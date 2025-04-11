import random
import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="function")
def product_simple(request_context: APIRequestContext):
    title = f"Simple Product {random.randint(100000, 999999)}"
    price = "19.99"
    product_simple = {"title": title, "price": price, "id": None}

    yield product_simple

    if product_simple["id"]:
        response = request_context.delete(
            f"wp-json/wc/v3/products/{product_simple['id']}", data={"force": True}
        )
        assert response.ok

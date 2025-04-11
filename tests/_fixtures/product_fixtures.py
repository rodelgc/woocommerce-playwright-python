import random
import pytest
from playwright.sync_api import APIRequestContext


@pytest.fixture(scope="function")
def product_simple(request_context: APIRequestContext):
    title = f"Simple Product {random.randint(100000, 999999)}"
    price = "19.99"
    sku = f"sku-{random.randint(1000, 9999)}"
    tags = [f"tag-{random.randint(1000, 9999)}", f"tag-{random.randint(1000, 9999)}"]
    stock = "10"
    product = {
        "title": title,
        "price": price,
        "id": None,
        "sku": sku,
        "tags": tags,
        "stock": stock,
    }

    yield product

    if product["id"]:
        response = request_context.delete(
            f"wp-json/wc/v3/products/{product['id']}", data={"force": True}
        )
        assert response.ok

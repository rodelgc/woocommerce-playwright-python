import random
import pytest
from playwright.sync_api import APIRequestContext


def random_price() -> str:
    """Generate a random price for the product."""
    return f"{random.randint(100, 999)}.{random.randint(00, 99)}"


def random_sku() -> str:
    """Generate a random SKU for the product."""
    return f"sku-{random.randint(1000, 9999)}"


def random_tags(count: int) -> list:
    """Generate a list of random tags for the product."""
    return [f"tag-{random.randint(1000, 9999)}" for _ in range(count)]


def random_stock() -> str:
    """Generate a random stock quantity for the product."""
    return str(random.randint(10, 100))


def cleanup_product(product_id: int | None, request_context: APIRequestContext):
    """Cleanup function to delete the product after test."""
    if not product_id:
        return

    response = request_context.delete(
        f"wp-json/wc/v3/products/{product_id}", data={"force": True}
    )
    assert response.ok


@pytest.fixture(scope="function")
def product_simple(request_context: APIRequestContext):
    """Fixture to create a simple product for testing."""
    title = "Pride and Prejudice"
    price = random_price()
    sku = random_sku()
    tags = random_tags(3)
    stock = random_stock()
    product = {
        "title": title,
        "price": price,
        "id": None,
        "sku": sku,
        "tags": tags,
        "stock": stock,
    }

    yield product

    cleanup_product(product["id"], request_context)


@pytest.fixture(scope="function")
def product_variable(request_context: APIRequestContext):
    """Fixture to create a variable product for testing."""
    title = "The Chronicles of Narnia"
    attributes = [
        {
            "name": "Format",
            "values": "Hardcover | Paperback | eBook",
        },
        {
            "name": "Language",
            "values": "English | Spanish | French",
        },
        {
            "name": "Edition",
            "values": "First Edition | Revised Edition",
        },
    ]
    product = {"title": title, "id": None, "attributes": attributes}

    yield product

    cleanup_product(product["id"], request_context)

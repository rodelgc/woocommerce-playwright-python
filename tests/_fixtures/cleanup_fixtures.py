import pytest

from playwright.sync_api import APIRequestContext


def cleanup_products(request_context: APIRequestContext):
    path = "wp-json/wc/v3/products"

    # Get all products with any status except "trash"
    get_response = request_context.get(
        path, data={"per_page": 100, "include_status": "any", "_fields": "id"}
    )
    assert get_response.ok

    # Get all products with status "trash"
    get_response_trash = request_context.get(
        path, data={"per_page": 100, "include_status": "trash", "_fields": "id"}
    )
    assert get_response_trash.ok

    # Get all product ids
    products: list = get_response.json()
    products_trash: list = get_response_trash.json()
    product_ids = [product["id"] for product in products + products_trash]

    # Batch delete products
    if product_ids:
        batch_response = request_context.post(
            "wp-json/wc/v3/products/batch",
            data={"delete": product_ids},
        )
        assert batch_response.ok


@pytest.fixture(scope="session", autouse=True)
def cleanup_store(request_context: APIRequestContext):
    cleanup_products(request_context)

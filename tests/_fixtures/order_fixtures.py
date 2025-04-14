import pytest

from playwright.sync_api import APIRequestContext


def clean_up_order(order_id: int | None, request_context: APIRequestContext) -> None:
    if order_id:
        response = request_context.delete(
            f"wp-json/wc/v3/orders/{order_id}", data={"force": True}
        )
        assert response.ok


@pytest.fixture(scope="function")
def order_data(request_context: APIRequestContext):
    ord_data = {"id": None}

    yield ord_data

    clean_up_order(ord_data["id"], request_context)

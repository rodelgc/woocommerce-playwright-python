import re
import random
import pytest
from typing import Dict
from playwright.sync_api import Page, expect, APIRequestContext
from urllib.parse import urlparse, parse_qs


def extract_product_id(url: str) -> str:
    params = parse_qs(urlparse(url).query)
    id = params.get("post", [None])[0]
    return id


@pytest.fixture(scope="function")
def product(request_context: APIRequestContext):
    title = f"Simple Product {random.randint(100000, 999999)}"
    price = "19.99"
    product = {"title": title, "price": price, "id": None}

    yield product

    request_context.delete(
        f"wp-json/wc/v3/products/{product['id']}",
    )


def test_product_simple(merchant_page: Page, product: Dict[str, str | None]):
    merchant_page.goto("wp-admin/post-new.php?post_type=product")
    expect(merchant_page).to_have_title(re.compile("^Add new product"))
    merchant_page.get_by_label("Product name").fill(product["title"])
    merchant_page.get_by_label("Regular price ($)").fill(product["price"])
    merchant_page.locator('[name="publish"]').click()
    expect(merchant_page.get_by_text("Product published.")).to_be_visible()
    product["id"] = extract_product_id(merchant_page.url)

    merchant_page.goto("wp-admin/edit.php?post_type=product")
    expect(
        merchant_page.get_by_role("link", name=product["title"], exact=True)
    ).to_be_visible()

import re
from typing import Dict
from playwright.sync_api import Page, expect
from urllib.parse import urlparse, parse_qs


def extract_product_id(url: str) -> str:
    params = parse_qs(urlparse(url).query)
    id = params.get("post", [None])[0]
    return id


def test_can_add_new_product__simple(
    merchant_page: Page, product_simple: Dict[str, str | None]
):
    merchant_page.goto("wp-admin/post-new.php?post_type=product")
    expect(merchant_page).to_have_title(re.compile("^Add new product"))
    merchant_page.get_by_label("Product name").fill(product_simple["title"])
    merchant_page.get_by_label("Regular price ($)").fill(product_simple["price"])
    merchant_page.locator('[name="publish"]').click()
    expect(merchant_page.get_by_text("Product published.")).to_be_visible()
    product_simple["id"] = extract_product_id(merchant_page.url)

    merchant_page.goto("wp-admin/edit.php?post_type=product")
    expect(
        merchant_page.get_by_role("link", name=product_simple["title"], exact=True)
    ).to_be_visible()

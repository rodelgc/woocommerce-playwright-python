import re
import random
from playwright.sync_api import Page, expect
from urllib.parse import urlparse, parse_qs

PRODUCT_TITLE = f"Simple Product {random.randint(100000, 999999)}"
PRODUCT_PRICE = "19.99"


def extract_product_id(url: str) -> str:
    params = parse_qs(urlparse(url).query)
    product_id = params.get("post", [None])[0]
    return product_id


def test_product_simple(merchant_page: Page):
    merchant_page.goto("wp-admin/post-new.php?post_type=product")
    expect(merchant_page).to_have_title(re.compile("^Add new product"))
    merchant_page.get_by_label("Product name").fill(PRODUCT_TITLE)
    merchant_page.get_by_label("Regular price ($)").fill(PRODUCT_PRICE)
    merchant_page.locator('[name="publish"]').click()
    expect(merchant_page.get_by_text("Product published.")).to_be_visible()
    product_id = extract_product_id(merchant_page.url)
    print(f"Product ID: {product_id}")  # TODO Use on tear down

    merchant_page.goto("wp-admin/edit.php?post_type=product")
    expect(
        merchant_page.get_by_role("link", name=PRODUCT_TITLE, exact=True)
    ).to_be_visible()

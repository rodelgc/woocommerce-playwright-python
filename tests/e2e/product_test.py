import re
import pytest
import random
from playwright.sync_api import Page, expect

PRODUCT_TITLE = f"Simple Product {random.randint(100000, 999999)}"
PRODUCT_PRICE = "19.99"


@pytest.fixture(autouse=True)
def page(page: Page):
    auth_context = page.context.browser.new_context(
        storage_state="playwright/.auth/merchant.state.json"
    )
    merchant_page = auth_context.new_page()

    yield merchant_page

    # TODO tear down


def test_product_simple(page: Page, base_url):
    page.goto(f"{base_url}/wp-admin/post-new.php?post_type=product")
    expect(page).to_have_title(re.compile("^Add new product"))

    page.get_by_label("Product name").fill(PRODUCT_TITLE)
    page.get_by_label("Regular price ($)").fill(PRODUCT_PRICE)
    page.locator('[name="publish"]').click()
    expect(page.get_by_text("Product published.")).to_be_visible()

    page.goto(f"{base_url}/wp-admin/edit.php?post_type=product")
    expect(page.get_by_role("link", name=PRODUCT_TITLE, exact=True)).to_be_visible()

import re
from typing import Dict
from playwright.sync_api import Page, expect
from _helpers.product_helpers import extract_product_id_from_url


def test_can_add_new_product__simple(
    merchant_page: Page, product_simple: Dict[str, str | None]
):
    def goto_add_new_product_page_and_add_product():
        product_name_input = merchant_page.get_by_label("Product name")
        regular_price_input = merchant_page.get_by_label("Regular price ($)")
        publish_button = merchant_page.get_by_role("button", name="Publish", exact=True)
        product_published_message = merchant_page.get_by_text("Product published.")

        # Go to "Add new product" page.
        merchant_page.goto("wp-admin/post-new.php?post_type=product")
        expect(merchant_page).to_have_title(re.compile("^Add new product"))

        # Fill in the product details and submit.
        product_name_input.fill(product_simple["title"])
        regular_price_input.fill(product_simple["price"])
        publish_button.click()
        expect(product_published_message).to_be_visible()

        # Save product id.
        product_simple["id"] = extract_product_id_from_url(merchant_page.url)

    def goto_products_page_and_expect_product_saved():
        product_cell = merchant_page.get_by_role(
            "cell", name=f"{product_simple['title']} ID: {product_simple['id']}"
        )
        price_cell = merchant_page.locator(f"#post-{product_simple['id']}").get_by_role(
            "cell", name="$"
        )

        merchant_page.goto("wp-admin/edit.php?post_type=product")
        expect(product_cell).to_contain_text(product_simple["title"])
        product_cell.hover()
        expect(product_cell).to_contain_text("Edit")
        expect(product_cell).to_contain_text("Quick Edit")
        expect(product_cell).to_contain_text("Trash")
        expect(product_cell).to_contain_text("View")
        expect(product_cell).to_contain_text("Duplicate")
        expect(price_cell).to_contain_text(product_simple["price"])

    goto_add_new_product_page_and_add_product()
    goto_products_page_and_expect_product_saved()

import re
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, expect

from tests._models.merchant.products.add_new_product.product_data_section import (
    ProductDataSection,
)


class AddNewProductPage:
    """Page object for the Add New Product page in WooCommerce."""

    def __init__(self, page: Page):
        self.page = page
        self.product_data = ProductDataSection(page)

    def goto(self) -> None:
        path = "wp-admin/post-new.php?post_type=product"

        self.page.goto(path)
        expect(self.page).to_have_title(re.compile("^Add new product"))

    def fill_product_name(self, product_name: str) -> None:
        product_name_input = self.page.get_by_label("Product name")

        product_name_input.fill(product_name)

    def publish(self) -> None:
        publish_button = self.page.get_by_role("button", name="Publish", exact=True)
        publish_success_message = self.page.get_by_text("Product published.")

        publish_button.click()
        expect(publish_success_message).to_be_visible()

    def extract_product_id_from_url(self) -> str:
        params = parse_qs(urlparse(self.page.url).query)
        product_id = params.get("post", [None])[0]
        return product_id

    def fill_product_tags(self, tags: list[str]) -> None:
        for tag in tags:
            tag_input = self.page.get_by_role("combobox", name="Add new tag")
            tag_input.fill(tag)
            tag_input.press("Enter")
            expect(self.page.get_by_text(f"Remove term: {tag}")).to_be_visible()

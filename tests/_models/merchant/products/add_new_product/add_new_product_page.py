import re
from playwright.sync_api import Page, expect
from .product_data_section import ProductDataSection
from urllib.parse import urlparse, parse_qs


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
        id = params.get("post", [None])[0]
        return id

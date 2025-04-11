# pylint: disable=too-few-public-methods


from typing import Dict
from playwright.sync_api import Page, expect


class AllProductsTable:
    def __init__(self, page: Page):
        self.page = page

    def expect_product_listed(self, product: Dict[str, str | None]) -> None:
        product_cell = self.page.get_by_role(
            "cell", name=f"{product['title']} ID: {product['id']}"
        )
        price_cell = self.page.locator(f"#post-{product['id']}").get_by_role(
            "cell", name="$"
        )

        product_cell.hover()
        expect(product_cell).to_contain_text("Edit")
        expect(product_cell).to_contain_text("Quick Edit")
        expect(product_cell).to_contain_text("Trash")
        expect(product_cell).to_contain_text("View")
        expect(product_cell).to_contain_text("Duplicate")
        expect(price_cell).to_contain_text(product["price"])

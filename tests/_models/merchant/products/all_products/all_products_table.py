# pylint: disable=too-few-public-methods


from typing import Dict
from playwright.sync_api import Page, expect


class AllProductsTable:
    def __init__(self, page: Page):
        self.page = page

    def expect_product_listed(self, product: Dict[str, any]) -> None:
        row = self.page.locator(f"#post-{product['id']}")
        product_cell = self.page.get_by_role(
            "cell", name=f"{product['title']} ID: {product['id']}"
        )
        sku_cell = self.page.get_by_role("cell", name=product["sku"])
        stock_cell = row.get_by_role("cell", name="In stock")
        price_cell = row.get_by_role("cell", name="$")

        product_cell.hover()
        expect(product_cell).to_contain_text("Edit")
        expect(product_cell).to_contain_text("Quick Edit")
        expect(product_cell).to_contain_text("Trash")
        expect(product_cell).to_contain_text("View")
        expect(product_cell).to_contain_text("Duplicate")
        expect(sku_cell).to_be_visible()
        expect(stock_cell).to_be_visible()
        expect(price_cell).to_contain_text(product["price"])

        for tag in product["tags"]:
            expect(row).to_contain_text(tag)

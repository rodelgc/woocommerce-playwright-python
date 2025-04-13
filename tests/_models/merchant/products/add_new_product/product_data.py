from tests._models.merchant.products.add_new_product.product_data_attributes import (
    AttributesTab,
)
from tests._models.merchant.products.add_new_product.product_data_variations import (
    VariationsTab,
)

from playwright.sync_api import Page


class ProductData:
    """Page object for the Add new product page > Product Data section in WooCommerce."""

    def __init__(self, page: Page):
        self.page = page.locator("#woocommerce-product-data")
        self.product_type_select = self.page.get_by_label("Simple product Grouped")
        self.attributes_tab = AttributesTab(self.page)

    # Product type select
    def select_product_type_variable(self) -> None:
        self.product_type_select.select_option(label="Variable product")

    # General tab
    def fill_regular_price(self, regular_price: str) -> None:
        regular_price_input = self.page.get_by_label("Regular price ($)")
        regular_price_input.fill(regular_price)

    # Inventory tab
    def goto_inventory_tab(self) -> None:
        inventory_tab = self.page.get_by_role("link", name="Inventory")
        inventory_tab.click()

    def fill_sku(self, sku: str) -> None:
        sku_input = self.page.get_by_role("textbox", name="SKU")
        sku_input.fill(sku)

    def check_stock_management(self) -> None:
        stock_management_checkbox = self.page.get_by_role(
            "checkbox", name="Stock management"
        )
        stock_management_checkbox.check()

    def check_stock_status_in_stock(self) -> None:
        in_stock_checkbox = self.page.get_by_role("radio", name="In stock")
        in_stock_checkbox.check()

    def fill_stock_quantity(self, stock: str) -> None:
        stock_quantity_input = self.page.get_by_role("spinbutton", name="Quantity")
        stock_quantity_input.fill(stock)

    def goto_attributes_tab(self) -> AttributesTab:
        inventory_tab = self.page.get_by_role("link", name="Attributes")
        inventory_tab.click()
        return AttributesTab(self.page)

    def goto_variations_tab(self) -> VariationsTab:
        inventory_tab = self.page.get_by_role("link", name="Variations")
        inventory_tab.click()
        return VariationsTab(self.page)

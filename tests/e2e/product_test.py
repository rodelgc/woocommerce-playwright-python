from typing import Dict

from playwright.sync_api import Page, expect

from tests._models.merchant.products.add_new_product.add_new_product_page import (
    AddNewProductPage,
)
from tests._models.merchant.products.all_products.all_products_page import (
    AllProductsPage,
)


def test_can_add_new_product__simple(
    merchant_page: Page, customer_page: Page, product_data_simple: Dict[str, any]
):

    def add_new_simple_product() -> None:
        add_new_product_page = AddNewProductPage(merchant_page)
        product_data_section = add_new_product_page.product_data_section
        add_new_product_page.goto()
        add_new_product_page.fill_product_name(product_data_simple["title"])
        product_data_section.fill_regular_price(product_data_simple["price"])
        product_data_section.goto_inventory_tab()
        product_data_section.fill_sku(product_data_simple["sku"])
        product_data_section.check_stock_management()
        product_data_section.fill_stock_quantity(product_data_simple["stock"])
        add_new_product_page.fill_product_tags(product_data_simple["tags"])
        add_new_product_page.publish()
        product_data_simple["id"] = add_new_product_page.extract_product_id_from_url()

    def check_simple_product_on_all_products_page() -> str:
        all_products_page = AllProductsPage(merchant_page)
        all_products_page.goto()
        all_products_page.table.expect_product_listed(product_data_simple)
        product_url = all_products_page.table.get_product_url(product_data_simple["id"])
        return product_url

    def view_product_as_customer(product_url: str) -> None:
        customer_page.goto(product_url)
        expect(
            customer_page.get_by_text(product_data_simple["title"], exact=True)
        ).to_be_visible()
        expect(customer_page.get_by_text(product_data_simple["price"])).to_be_visible()

    add_new_simple_product()
    product_url = check_simple_product_on_all_products_page()
    view_product_as_customer(product_url)

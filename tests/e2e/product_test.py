from typing import Dict

from playwright.sync_api import Page

from tests._models.merchant.products.add_new_product.add_new_product_page import (
    AddNewProductPage,
)
from tests._models.merchant.products.all_products.all_products_page import (
    AllProductsPage,
)


def test_can_add_new_product__simple(
    merchant_page: Page, product_simple: Dict[str, str | None]
):
    add_new_product_page = AddNewProductPage(merchant_page)
    all_products_page = AllProductsPage(merchant_page)

    # Add new product.
    add_new_product_page.goto()
    add_new_product_page.fill_product_name(product_simple["title"])
    add_new_product_page.product_data.fill_regular_price(product_simple["price"])
    add_new_product_page.publish()
    product_simple["id"] = add_new_product_page.extract_product_id_from_url()

    # Go to All Products page and check if the product is listed.
    all_products_page.goto()
    all_products_page.table.expect_product_listed(product_simple)

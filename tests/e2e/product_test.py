from typing import Dict

from playwright.sync_api import Page, expect

from tests._models.merchant.products.add_new_product.add_new_product_page import (
    AddNewProductPage,
)
from tests._models.merchant.products.all_products.all_products_page import (
    AllProductsPage,
)


def test_can_add_new_product__simple(
    merchant_page: Page, customer_page: Page, product_simple: Dict[str, any]
):
    add_new_product_page = AddNewProductPage(merchant_page)
    all_products_page = AllProductsPage(merchant_page)

    # Add new product.
    add_new_product_page.goto()
    add_new_product_page.fill_product_name(product_simple["title"])
    add_new_product_page.product_data.fill_regular_price(product_simple["price"])
    add_new_product_page.product_data.goto_inventory_tab()
    add_new_product_page.product_data.fill_sku(product_simple["sku"])
    add_new_product_page.product_data.check_stock_management()
    add_new_product_page.product_data.fill_stock_quantity(product_simple["stock"])
    add_new_product_page.fill_product_tags(product_simple["tags"])
    add_new_product_page.publish()
    product_simple["id"] = add_new_product_page.extract_product_id_from_url()

    # Go to All Products page and check if the product is listed.
    all_products_page.goto()
    all_products_page.table.expect_product_listed(product_simple)

    # View product from customer side.
    product_url = all_products_page.table.get_product_url(product_simple["id"])
    customer_page.goto(product_url)
    expect(
        customer_page.get_by_text(product_simple["title"], exact=True)
    ).to_be_visible()
    expect(customer_page.get_by_text(product_simple["price"])).to_be_visible()


def test_can_add_new_product__variable(
    merchant_page: Page,
    product_variable: Dict[str, any],
):
    add_new_product_page = AddNewProductPage(merchant_page)
    product_data_section = add_new_product_page.product_data

    def add_new_variable_product():
        add_new_product_page.goto()
        add_new_product_page.fill_product_name(product_variable["title"])
        product_data_section.select_product_type_variable()

    def add_attributes():
        attributes_tab = product_data_section.goto_attributes_tab()
        for attribute in product_variable["attributes"]:
            attributes_tab.add_new_attribute_using_form(
                attribute_name=attribute["name"],
                attribute_values=attribute["values"],
            )
            expect(
                attributes_tab.get_saved_attribute_heading(
                    attribute_name=attribute["name"]
                )
            ).to_be_visible()

    def generate_variations():
        variations_tab = product_data_section.goto_variations_tab()
        variations_tab.generate_variations()
        expect(variations_tab.count_variations()).to_have_count(
            len(product_variable["variations"])
        )

    add_new_variable_product()
    add_attributes()
    generate_variations()

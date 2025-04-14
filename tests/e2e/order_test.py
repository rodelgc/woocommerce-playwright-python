from typing import Dict
from playwright.sync_api import Page

from tests._models.customer.cart_page import CartPage
from tests._models.customer.product_page import ProductPage


def test_customer_can_add_product_to_cart(
    customer_page: Page,
    product: Dict[str, any],
    customer: Dict[str, any],
) -> None:
    # Expected values to check
    expected_quantity = "3"
    expected_item_total = "89.94"

    def goto_product_page_and_add_to_cart() -> CartPage:
        # Product data
        product_url = product["permalink"]

        # User actions
        product_page = ProductPage(customer_page)
        product_page.goto(product_url)
        product_page.fill_quantity(expected_quantity)
        product_page.add_to_cart()
        cart_page = product_page.click_view_cart_link()
        return cart_page

    def check_cart_details(cart_page: CartPage) -> None:
        # Product data
        product_name = product["name"]
        product_regular_price = product["regular_price"]

        # User actions
        cart_item = cart_page.get_cart_item_by_product_name(product_name)
        cart_item.has_expected_product_link(product_name)
        cart_item.has_expected_quantity(expected_quantity)
        cart_item.has_expected_price(product_regular_price)
        cart_item.shows_remove_item_button()
        cart_item.has_expected_total(expected_item_total)

    def checkout_order(cart_page: CartPage) -> None:
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_billing_form(customer)

    cart_page = goto_product_page_and_add_to_cart()
    check_cart_details(cart_page)
    checkout_order(cart_page)

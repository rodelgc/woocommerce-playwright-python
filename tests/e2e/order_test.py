from typing import Dict
from playwright.sync_api import Page

from tests._models.customer.cart_page import CartPage
from tests._models.customer.order_confirmation_page import OrderConfirmationPage
from tests._models.customer.product_page import ProductPage


def test_customer_can_add_product_to_cart(
    customer_page: Page,
    order_data: Dict[str, any],
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

    def proceed_to_checkout_and_place_order(
        cart_page: CartPage,
    ) -> OrderConfirmationPage:
        checkout_page = cart_page.proceed_to_checkout()
        checkout_page.fill_billing_form(customer)
        order_confirmation_page = checkout_page.place_order()
        return order_confirmation_page

    def check_details_in_order_confirmation_page(
        order_confirmation_page: OrderConfirmationPage,
    ) -> None:
        billing_details = customer["billing"]
        order_confirmation_page.has_expected_total(expected_item_total)
        order_confirmation_page.has_expected_email(billing_details["email"])
        order_confirmation_page.has_expected_cod_payment_method()
        order_confirmation_page.has_expected_product_link(product["name"])
        order_confirmation_page.has_expected_customer_billing_details(customer)
        order_data["id"] = order_confirmation_page.get_order_number()

    cart_page = goto_product_page_and_add_to_cart()
    check_cart_details(cart_page)
    order_confirmation_page = proceed_to_checkout_and_place_order(cart_page)
    check_details_in_order_confirmation_page(order_confirmation_page)

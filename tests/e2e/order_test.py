import re
from typing import Dict
from playwright.sync_api import Page, expect


def test_customer_can_add_product_to_cart(
    customer_page: Page,
    product: Dict[str, any],
    customer: Dict[str, any],
) -> None:
    # Product data
    expected_quantity = "3"
    expected_item_total = "89.94"

    def goto_product_page_and_add_to_cart() -> None:
        # Locators in Product page
        quantity_input = customer_page.get_by_role(
            "spinbutton", name="Product quantity"
        )
        add_to_cart_button = customer_page.get_by_role("button", name="Add to cart")
        add_to_cart_success_message = customer_page.get_by_role("alert")
        view_cart_link = customer_page.get_by_role("link", name="View cart")

        # Product data
        product_url = product["permalink"]

        customer_page.goto(product_url)
        quantity_input.fill(expected_quantity)
        add_to_cart_button.click()
        expect(add_to_cart_success_message).to_contain_text(
            re.compile(r"(has|have) been added to your cart.")
        )
        expect(view_cart_link).to_be_visible()
        view_cart_link.click()
        expect(customer_page).to_have_url(re.compile(r".*/cart"))
        expect(customer_page).to_have_title(re.compile(r"^Cart"))

    def check_cart_details() -> None:
        product_name = product["name"]
        product_regular_price = product["regular_price"]

        cart_cell_product_data = customer_page.get_by_role("cell", name=product_name)
        cart_product_link = cart_cell_product_data.get_by_role(
            "link", name=product_name
        )
        cart_quantity_input = cart_cell_product_data.get_by_role(
            "spinbutton", name="Quantity of"
        )
        cart_unit_price = cart_cell_product_data.get_by_text("$")
        cart_remove_item_button = cart_cell_product_data.get_by_role(
            "button", name="Remove"
        )
        cart_item_total = customer_page.get_by_role(
            "cell", name=f"${expected_item_total}"
        )

        expect(cart_product_link).to_be_visible()
        expect(cart_quantity_input).to_have_value(expected_quantity)
        expect(cart_unit_price).to_contain_text(product_regular_price)
        expect(cart_remove_item_button).to_be_visible()
        expect(cart_item_total).to_be_visible()

    def checkout_order() -> None:
        customer_page.get_by_role("link", name="Proceed to Checkout").click()

        # Checkout page locators
        expect(customer_page).to_have_url(re.compile(r".*/checkout"))
        expect(customer_page).to_have_title(re.compile(r"^Checkout"))

        # Fill in billing details
        customer_page.get_by_role("textbox", name="Email address").fill(
            customer["email"]
        )
        customer_page.get_by_label("Country/Region").select_option(value="US")
        customer_page.get_by_role("textbox", name="First name").fill(
            customer["billing"]["first_name"]
        )
        customer_page.get_by_role("textbox", name="Last name").fill(
            customer["billing"]["last_name"]
        )
        customer_page.get_by_role("textbox", name="Address", exact=True).fill(
            customer["billing"]["address_1"]
        )
        customer_page.get_by_role("textbox", name="City").fill(
            customer["billing"]["city"]
        )
        customer_page.get_by_label("State").select_option(value="CA")
        customer_page.get_by_role("textbox", name="ZIP Code").fill(
            customer["billing"]["postcode"]
        )
        customer_page.get_by_role("textbox", name="Phone (optional)").fill(
            customer["billing"]["phone"]
        )

    goto_product_page_and_add_to_cart()
    check_cart_details()
    checkout_order()

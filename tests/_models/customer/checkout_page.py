import re
from typing import Dict
from playwright.sync_api import Page, expect

from tests._models.customer.order_confirmation_page import OrderConfirmationPage


class CheckoutPage:

    def __init__(self, page: Page):
        self.page = page

        # Make sure Checkout page is loaded before proceeding.
        expect(self.page).to_have_url(re.compile(r".*/checkout"))
        expect(self.page).to_have_title(re.compile(r"^Checkout"))

    def fill_billing_form(self, customer: Dict[str, any]) -> None:
        # Locators
        email = self.page.get_by_role("textbox", name="Email address")
        country = self.page.get_by_label("Country/Region")
        first_name = self.page.get_by_role("textbox", name="First name")
        last_name = self.page.get_by_role("textbox", name="Last name")
        address_line_1 = self.page.get_by_role("textbox", name="Address", exact=True)
        city = self.page.get_by_role("textbox", name="City")
        state = self.page.get_by_label("State")
        postcode = self.page.get_by_role("textbox", name="ZIP Code")
        phone = self.page.get_by_role("textbox", name="Phone (optional)")

        # Actions
        email.fill(customer["email"])
        country.select_option(value=customer["billing"]["country"])
        first_name.fill(customer["billing"]["first_name"])
        last_name.fill(customer["billing"]["last_name"])
        address_line_1.fill(customer["billing"]["address_1"])
        city.fill(customer["billing"]["city"])
        state.select_option(value=customer["billing"]["state"])
        postcode.fill(customer["billing"]["postcode"])
        phone.fill(customer["billing"]["phone"])

    def select_payment_method_cod(self) -> None:
        cod_checkbox = self.page.get_by_role("radio", name="Cash on delivery")
        cod_description = self.page.get_by_text("Pay with cash upon delivery.")

        cod_checkbox.check()
        expect(cod_description).to_be_visible()

    def place_order(self) -> OrderConfirmationPage:
        place_order_button = self.page.get_by_role("button", name="Place Order")
        place_order_button.click()
        return OrderConfirmationPage(self.page)

import re
from re import Match
from typing import Dict
from playwright.sync_api import Page, expect


class OrderConfirmationPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        # Make sure Order Confirmation page was loaded.
        expect(self.page).to_have_title("Order Confirmation")
        expect(self.page).to_have_url(re.compile(r".*order-received/\d+"))
        expect(self.page.get_by_role("heading", name="Order received")).to_be_visible()

    def get_order_number(self) -> int:
        order_number_cell = self.page.get_by_text(re.compile(r"Order #: \d+"))
        order_number_text = order_number_cell.text_content()
        order_number_match: Match = re.search(r"\d+", order_number_text)

        if not order_number_match:
            raise ValueError("Cannot retrieve order number")

        order_number = int(order_number_match.group(0))
        return order_number

    def has_expected_total(self, expected_total: str) -> None:
        total_cell = self.page.get_by_role("listitem").filter(has_text="Total: $")
        expect(total_cell).to_contain_text(expected_total)

    def has_expected_email(self, expected_email: str) -> None:
        email_cell = self.page.get_by_text(re.compile(r"Email: .*"))
        expect(email_cell).to_contain_text(expected_email)

    def has_expected_cod_payment_method(self) -> None:
        payment_method_cell = self.page.get_by_text("Payment: Cash on delivery")
        expect(payment_method_cell).to_be_visible()

    def has_expected_product_link(self, expected_product_name: str) -> None:
        product_name_link = self.page.get_by_role("link", name=expected_product_name)
        expect(product_name_link).to_be_visible()

    def has_expected_customer_billing_details(self, customer: Dict[str, any]) -> None:
        billing = customer["billing"]
        first_name = billing["first_name"]
        last_name = billing["last_name"]
        address_1 = billing["address_1"]
        city = billing["city"]
        state = billing["state"]
        postcode = billing["postcode"]
        phone = billing["phone"]

        billing_container = self.page.locator(
            "[data-block-name='woocommerce/order-confirmation-billing-address']"
        )

        expect(billing_container).to_contain_text(first_name)
        expect(billing_container).to_contain_text(last_name)
        expect(billing_container).to_contain_text(address_1)
        expect(billing_container).to_contain_text(city)
        expect(billing_container).to_contain_text(state)
        expect(billing_container).to_contain_text(postcode)
        expect(billing_container).to_contain_text(phone)

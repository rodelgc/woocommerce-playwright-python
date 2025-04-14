import re
from playwright.sync_api import Page, expect, Locator
from tests._models.customer.checkout_page import CheckoutPage


class CartItem:

    def __init__(self, page: Page):
        self.cart_item = page

    def has_expected_product_link(self, expected_product_name: str) -> None:
        product_link = self.cart_item.get_by_role("link", name=expected_product_name)
        expect(product_link).to_be_visible()

    def has_expected_quantity(self, expected_quantity: str) -> None:
        quantity_input = self.cart_item.get_by_role("spinbutton", name="Quantity of")
        expect(quantity_input).to_have_value(expected_quantity)

    def has_expected_price(self, expected_price: str) -> None:
        price = self.cart_item.get_by_text("$").first
        expect(price).to_contain_text(expected_price)

    def has_expected_total(self, expected_total: str) -> None:
        total = self.cart_item.get_by_text("$").last
        expect(total).to_contain_text(expected_total)

    def shows_remove_item_button(self) -> None:
        remove_item_button = self.cart_item.get_by_role("button", name="Remove")
        expect(remove_item_button).to_be_visible()


class CartPage:

    def __init__(self, page: Page) -> None:
        self.page = page

        # Assertions to ensure the page is loaded
        expect(page).to_have_url(re.compile(r".*/cart"))
        expect(page).to_have_title(re.compile(r"^Cart"))

    @property
    def proceed_to_checkout_button(self) -> Locator:
        return self.page.get_by_role("link", name="Proceed to Checkout")

    def get_cart_item_by_product_name(self, product_name: str) -> CartItem:
        cart_item = self.page.get_by_role("row", name=product_name)
        expect(cart_item).to_be_visible()
        return CartItem(cart_item)

    def proceed_to_checkout(self) -> CheckoutPage:
        self.proceed_to_checkout_button.click()
        return CheckoutPage(self.page)

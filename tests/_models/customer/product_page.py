import re
from playwright.sync_api import Page, Locator, expect
from tests._models.customer.cart_page import CartPage


class ProductPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    # ----------------------------
    # Locators
    # ----------------------------
    def __view_cart_link(self) -> Locator:
        return self.page.get_by_role("link", name="View cart")

    # ----------------------------
    # Actions
    # ----------------------------
    def goto(self, product_url: str) -> None:
        self.page.goto(product_url)

    def fill_quantity(self, quantity: str) -> None:
        quantity_input = self.page.get_by_role("spinbutton", name="Product quantity")
        quantity_input.fill(quantity)

    def add_to_cart(self) -> None:
        add_to_cart_button = self.page.get_by_role("button", name="Add to cart")
        add_to_cart_success_message = self.page.get_by_role("alert")
        view_cart_link = self.__view_cart_link()

        add_to_cart_button.click()
        expect(add_to_cart_success_message).to_contain_text(
            re.compile(r"(has|have) been added to your cart.")
        )
        expect(view_cart_link).to_be_visible()

    def click_view_cart_link(self) -> CartPage:
        view_cart_link = self.__view_cart_link()
        view_cart_link.click()
        return CartPage(self.page)

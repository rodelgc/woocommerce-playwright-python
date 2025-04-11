# pylint: disable=too-few-public-methods

from playwright.sync_api import Page


class ProductDataSection:
    """Page object for the Add new product page > Product Data section in WooCommerce."""

    def __init__(self, page: Page):
        self.page = page

    def fill_regular_price(self, regular_price: str) -> None:
        regular_price_input = self.page.get_by_label("Regular price ($)")

        regular_price_input.fill(regular_price)

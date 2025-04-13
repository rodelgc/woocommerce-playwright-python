from playwright.sync_api import Page, Locator


class VariationsTab:
    """Page object for the Variations tab in the Product Data section in WooCommerce."""

    def __init__(self, page: Page):
        self.variations_tab = page.locator("#variable_product_options")

    def generate_variations(self) -> None:
        generate_variations_button = self.variations_tab.get_by_role(
            "button", name="Generate variations"
        )
        self.variations_tab.page.on("dialog", lambda dialog: dialog.accept())
        generate_variations_button.click()

    def count_variations(self) -> Locator:
        return self.variations_tab.get_by_role("heading", name="Edit Remove")

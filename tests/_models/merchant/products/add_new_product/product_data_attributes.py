from playwright.sync_api import Page, Locator


class AttributesTab:
    def __init__(self, page: Page):
        self.page = page.locator("#product_attributes")

    def add_new_attribute_using_form(
        self, attribute_name: str, attribute_values: str
    ) -> None:
        """Fill the form to add a new attribute and save it."""
        attribute_name_input = self.page.get_by_role(
            "row", name="Name: Value(s):"
        ).get_by_placeholder("e.g. length or weight")
        attribute_values_input = self.page.get_by_role(
            "textbox", name="Enter options for customers"
        )
        used_for_variations_checkbox = self.page.get_by_role(
            "checkbox", name="Used for variations"
        ).last
        save_attributes_button = self.page.get_by_role("button", name="Save attributes")
        new_attribute_heading = self.page.get_by_role(
            "heading", name="Remove New attribute"
        )
        add_new_button = self.page.get_by_role("button", name="Add new")

        if not new_attribute_heading.is_visible():
            add_new_button.click()

        attribute_name_input.press_sequentially(attribute_name)
        attribute_values_input.press_sequentially(attribute_values)
        used_for_variations_checkbox.check()
        save_attributes_button.click()

    def saved_attribute_with_name(self, attribute_name: str) -> Locator:
        """Return a page locator for the saved attribute with the given name."""
        saved_attributes_headings = self.page.get_by_role("heading", name="Remove")

        return saved_attributes_headings.filter(has_text=attribute_name)

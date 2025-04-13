from typing import Dict
from playwright.sync_api import Page


class AttributesTab:
    def __init__(self, page: Page):
        self.page = page.locator("#product_attributes")

    def add_new_attribute_using_form(
        self, attribute_name: str, attribute_values: str
    ) -> None:
        """Fill the form to add a new attribute and save it."""

        # Locators
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

        # Click "Add new" button only if the new attribute form is not visible.
        if not new_attribute_heading.is_visible():
            add_new_button.click()

        # Fill the form and save.
        attribute_name_input.press_sequentially(attribute_name)
        attribute_values_input.press_sequentially(attribute_values)
        used_for_variations_checkbox.check()
        save_attributes_button.click()

    def is_attribute_saved(self, attribute: Dict[str, any]) -> bool:
        """Check if the attribute is saved in the attributes tab."""

        # Attribute properties
        attribute_name = attribute["name"]
        attribute_values = attribute["values"]

        # Locators
        saved_attribute_heading = self.page.get_by_role("heading", name="Remove")
        saved_attribute_name = self.page.get_by_role(
            "cell", name=attribute_name
        ).get_by_placeholder("e.g. length or weight")
        saved_attribute_values = self.page.get_by_role(
            "cell", name=f"Value(s): {attribute_values}"
        )
        used_for_variations_checkbox = (
            self.page.get_by_role("table")
            .filter(has_text=attribute_values)
            .get_by_role("checkbox", name="Used for variations")
        )

        return (
            saved_attribute_heading.is_visible()
            and saved_attribute_name.is_visible()
            and saved_attribute_values.is_visible()
            and used_for_variations_checkbox.is_checked()
        )

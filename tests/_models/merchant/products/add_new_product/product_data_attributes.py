from playwright.sync_api import Page, Locator


class AttributesTab:
    def __init__(self, page: Page):
        self.attributes_tab = page.locator("#product_attributes")

    def add_new_attribute_using_form(
        self, attribute_name: str, attribute_values: str
    ) -> None:
        """Fill the form to add a new attribute and save it."""

        # Locators
        attribute_name_input = self.attributes_tab.get_by_role(
            "row", name="Name: Value(s):"
        ).get_by_placeholder("e.g. length or weight")
        attribute_values_input = self.attributes_tab.get_by_role(
            "textbox", name="Enter options for customers"
        )
        used_for_variations_checkbox = self.attributes_tab.get_by_role(
            "checkbox", name="Used for variations"
        ).last
        save_attributes_button = self.attributes_tab.get_by_role(
            "button", name="Save attributes"
        )
        new_attribute_heading = self.attributes_tab.get_by_role(
            "heading", name="Remove New attribute"
        )
        add_new_button = self.attributes_tab.get_by_role("button", name="Add new")

        # Click "Add new" button only if the new attribute form is not visible.
        if not new_attribute_heading.is_visible():
            add_new_button.click()

        # Fill the form and save.
        attribute_name_input.press_sequentially(attribute_name)
        attribute_values_input.press_sequentially(attribute_values)
        used_for_variations_checkbox.check()

        # Wait for the request to finish after clicking the save button.
        with self.attributes_tab.page.expect_request_finished(
            lambda request: "admin-ajax.php" in request.url
            and request.method == "POST"
            and "action=woocommerce_save_attributes" in (request.post_data or "")
        ):
            save_attributes_button.click()

    def get_saved_attribute_heading(self, attribute_name: str) -> Locator:
        return self.attributes_tab.get_by_role(
            "heading", name=f"Remove {attribute_name}"
        )

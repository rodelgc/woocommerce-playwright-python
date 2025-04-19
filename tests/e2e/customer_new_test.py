from playwright.sync_api import Page, expect


def test_guest_can_register(page: Page):
    page.goto("my-account")

    # ---------------------------------
    # Registration form.
    # ---------------------------------
    # -- Customer data
    customer_registration_data = {
        "first_name": "Cullen",
        "last_name": "Cuomo",
        "email": "new_customer_random@example.com",
        "password": "@awsdfIllo.*fasdfsaf",
    }

    # -- Locators
    email_input = page.get_by_role(
        "textbox", name="Email address  Required", exact=True
    )
    password_input = page.locator("#reg_password")
    register_button = page.get_by_role("button", name="Register")

    # -- Actions
    email_input.fill(customer_registration_data["email"])
    password_input.fill(customer_registration_data["password"])
    register_button.click()

    # ---------------------------------
    # My account dashboard page
    # ---------------------------------
    # Customer data
    new_customer_username = customer_registration_data["email"].split("@", maxsplit=1)[
        0
    ]

    # Locators
    greeting = page.get_by_text("Hello")
    heading = page.get_by_role("heading", name="My account")
    log_out_link = page.get_by_label("Account pages").get_by_role(
        "link", name="Log out"
    )

    # Actions
    expect(heading).to_be_visible()
    expect(greeting).to_contain_text(new_customer_username)
    expect(log_out_link).to_be_visible()

    # ---------------------------------
    # My Account > Account details page
    # ---------------------------------
    # Locators
    account_details_link = page.get_by_role("link", name="Account details", exact=True)
    heading_account_details = page.get_by_role("heading", name="Account details")
    display_name_textbox = page.get_by_role("textbox", name="Display name")
    email_address_textbox = page.get_by_role("textbox", name="Email address")
    first_name_textbox = page.get_by_role("textbox", name="First name")
    last_name_textbox = page.get_by_role("textbox", name="Last name")
    save_changes_button = page.get_by_role("button", name="Save changes")

    # Actions
    account_details_link.click()
    expect(heading_account_details).to_be_visible()
    expect(display_name_textbox).to_have_value(new_customer_username)
    expect(email_address_textbox).to_have_value(customer_registration_data["email"])
    success_message = page.get_by_text("Account details changed")

    first_name_textbox.fill(customer_registration_data["first_name"])
    last_name_textbox.fill(customer_registration_data["last_name"])
    save_changes_button.click()
    expect(success_message).to_be_visible()

    # ---------------------------------
    # Cleanup customer
    # ---------------------------------
    # todo

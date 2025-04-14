import os

import pytest

from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext

# Load environment variables
load_dotenv("local.env")
WORDPRESS_CUSTOMER_EMAIL = os.getenv("WORDPRESS_CUSTOMER_EMAIL")


@pytest.fixture(scope="session")
def customer(request_context: APIRequestContext):
    data = {
        "billing": {
            "first_name": "Custer",
            "last_name": "Curry",
            "company": "Automattic Inc.",
            "address_1": "#60 Suite 100, Main Street",
            "address_2": "",
            "city": "San Francisco",
            "postcode": "94116",
            "country": "US",
            "state": "CA",
            "phone": "(415) 555-1234",
        },
    }

    # Get customer ID by email
    response_list_customers = request_context.get(
        "wp-json/wc/v3/customers",
        data={
            "per_page": 100,
            "email": WORDPRESS_CUSTOMER_EMAIL,
            "_fields": ["id", "email"],
            "role": "all",
        },
    )
    assert response_list_customers.ok
    customer_matches = response_list_customers.json()
    assert (
        len(customer_matches) == 1
    ), f"No customer found with the specified email: {WORDPRESS_CUSTOMER_EMAIL}"

    customer_matches: list = response_list_customers.json()
    customer_id = customer_matches[0]["id"]

    # Update customer data
    response_update_customer = request_context.put(
        f"/wp-json/wc/v3/customers/{customer_id}",
        data=data,
    )
    assert response_update_customer.ok
    customer = response_update_customer.json()

    yield customer

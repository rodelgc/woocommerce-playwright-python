from typing import List, Dict
import pytest
from playwright.sync_api import APIRequestContext


def reset_payment_cod(request_context: APIRequestContext) -> None:
    path = "wp-json/wc/v3/payment_gateways"

    def all_payment_gateways() -> List[str]:
        data = {"_fields": ["id", "enabled"]}

        response = request_context.get(path, data=data)

        assert response.ok

        payment_gateways: List[Dict[str, str | bool]] = response.json()

        return [pg["id"] for pg in payment_gateways]

    def enable_cod_only(ids: List[str]) -> None:
        for _id in ids:
            is_cod = _id == "cod"
            data = {"enabled": is_cod, "_fields": ["id", "enabled"]}

            response = request_context.put(f"{path}/{_id}", data=data)

            assert response.ok
            assert response.json()["enabled"] == is_cod

    ids = all_payment_gateways()
    enable_cod_only(ids)


def enable_my_account_registration(request_context: APIRequestContext) -> None:
    path = "wp-json/wc/v3/settings/account/woocommerce_enable_myaccount_registration"
    data = {"value": "yes"}

    response = request_context.put(path, data=data)

    assert response.ok
    assert response.json()["value"] == "yes"


@pytest.fixture(scope="session", autouse=True)
def reset_settings(request_context: APIRequestContext):
    reset_payment_cod(request_context)
    enable_my_account_registration(request_context)

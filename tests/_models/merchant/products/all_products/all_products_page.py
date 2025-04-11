import re
from playwright.sync_api import Page, expect
from .all_products_table import AllProductsTable


class AllProductsPage:

    def __init__(self, page: Page):
        self.page = page
        self.table = AllProductsTable(page)

    def goto(self) -> None:
        path = "wp-admin/edit.php?post_type=product"

        self.page.goto(path)
        expect(self.page).to_have_title(re.compile("^Products"))

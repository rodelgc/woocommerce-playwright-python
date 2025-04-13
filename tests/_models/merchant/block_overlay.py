from playwright.sync_api import Page, expect


class BlockOverlay:
    def __init__(self, page: Page):
        self.page = page

    def wait_until_gone(self) -> None:
        """Wait until all block overlays are gone."""

        block_overlays = self.page.locator(".blockUI.blockOverlay")
        count = block_overlays.count()

        for i in range(count):
            expect(block_overlays.nth(i)).not_to_be_visible()

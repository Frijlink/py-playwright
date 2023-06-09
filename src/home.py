import os

URL = os.getenv("BASE_URL")

class HomePage:
    def __init__(self, page):
        self.page = page
        self.section_header = page.locator('h3.boards-page-section-header-name')
        self.new_board_btn = page.locator('[data-testid="create-board-tile"]')
        self.new_board_name_input = page.locator('[data-testid="create-board-title-input"]')
        self.select_visibility_dropdown = page.locator('[id$="create-board-select-visibility"] > div > div > div:nth-child(1)')
        self.visibility_private_btn = page.locator('#react-select-4-option-0 li')
        self.visibility_workspace_btn = page.locator('#react-select-4-option-1 li')
        self.visibility_public_btn = page.locator('#react-select-4-option-2 li')
        self.create_new_board_submit_btn = page.locator('[data-testid="create-board-submit-button"]')
        self.board_tile_title = page.locator('.board-tile-details-name')

    def goto(self):
        self.page.goto(URL)

    def create_new_board(self, name, background_colour):
        self.new_board_btn.click()
        self.page.locator(f"button[title=\"{background_colour}\"]").click()
        self.new_board_name_input.type(name, delay=50)
        self.create_new_board_submit_btn.wait_for(state="attached")
        self.create_new_board_submit_btn.click()
        self.page.wait_for_url(f"**/{name.lower()}")

    def get_all_board_names(self):
        return self.board_tile_title.all_inner_texts() if (self.board_tile_title.is_visible()) else []


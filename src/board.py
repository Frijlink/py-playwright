class BoardPage:
    def __init__(self, page):
        self.page = page
        self.main_title = page.locator('[data-testid="board-name-display"]')
        self.board_name_input = page.locator('[data-testid="board-name-input"]')
        self.board = page.locator('#board')
        self.left_menu = page.locator('[data-testid="workspace-boards-and-views-lists"]')
        self.close_board_message = page.locator('[data-testid="close-board-big-message"]')
        self.delete_board_btn = page.locator('[data-testid="close-board-delete-board-button"]')
        self.delete_board_confirm_btn = page.locator('[data-testid="close-board-delete-board-confirm-button"]')

    def wait_for_page_loaded(self):
        self.board.wait_for()
        self.left_menu.wait_for()

    def update_board_name(self, new_name):
        self.main_title.click()
        self.board_name_input.clear()
        self.board_name_input.fill(new_name)
        self.page.keyboard.press("Enter")

    def delete_board(self):
        self.delete_board_btn.click()
        self.delete_board_confirm_btn.click()
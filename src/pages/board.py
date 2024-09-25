class BoardPage:
    def __init__(self, page):
        self.page = page
        self.main_title = page.get_by_test_id('board-name-display')
        self.board_name_input = page.get_by_test_id('board-name-input')
        self.board = page.locator('#board')
        self.left_menu = page.get_by_test_id('workspace-boards-and-views-lists')
        self.board_menu = page.get_by_label('Show menu')
        self.close_board_message = page.locator('#content-wrapper p')
        self.delete_board_btn = page.get_by_test_id('close-board-delete-board-button')
        self.delete_board_confirm_btn = page.get_by_test_id('close-board-delete-board-confirm-button')
        self.trello_btn = page.get_by_label('Back to home')

    def wait_for_page_loaded(self):
        self.board.wait_for()
        self.left_menu.wait_for()

    def update_board_name(self, new_name):
        self.main_title.click()
        self.board_name_input.clear()
        self.board_name_input.fill(new_name)
        self.page.keyboard.press("Enter")

    def delete_board(self):
        self.board_menu.click()
        self.delete_board_btn.click()
        self.delete_board_confirm_btn.click()
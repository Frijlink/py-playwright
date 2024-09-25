class WorkspaceNavComponent:
    def __init__(self, page):
        self.page = page
        self.nav = page.get_by_test_id('workspace-navigation-nav')
        self.current_board = page.get_by_label('(currently active)')
        self.board_actions_menu_btn = page.get_by_label('Board actions menu')
        self.close_board_btn = page.get_by_label('Close board')
        self.close_btn = page.get_by_test_id('popover-close-board-confirm')

    def close_current_board(self):
        self.current_board.hover()
        self.board_actions_menu_btn.click()
        self.close_board_btn.click()
        self.close_btn.click()
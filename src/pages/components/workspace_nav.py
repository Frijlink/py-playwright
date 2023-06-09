class WorkspaceNavComponent:
    def __init__(self, page):
        self.page = page
        self.nav = page.locator('nav[data-testid="workspace-navigation-nav"]')
        self.current_board = page.locator('[aria-label$="(currently active)"]')
        self.board_actions_menu_btn = page.locator('[aria-label="Board actions menu"]')
        self.close_board_btn = page.locator('[aria-label="Close board"]')
        self.close_btn = page.locator('[title="Close"]')

    def close_current_board(self):
        self.current_board.hover()
        self.board_actions_menu_btn.click()
        self.close_board_btn.click()
        self.close_btn.click()
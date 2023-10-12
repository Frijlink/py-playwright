class HeaderComponent:
    def __init__(self, page):
        self.page = page
        self.login_btn = page.locator('a[class^="Buttonsstyles"][href*="/login"]')
        self.member_info_btn = page.locator('[data-testid="header-member-menu-button"]')
        self.member_info_logout_btn = page.locator('[data-testid="account-menu-logout"]')
        self.logout_submit_btn = page.locator('button#logout-submit')

    def log_out(self):
        self.member_info_btn.click()
        self.member_info_logout_btn.click()
        self.logout_submit_btn.click()
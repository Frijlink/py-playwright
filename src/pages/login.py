class LoginPage:
    def __init__(self, page):
        self.page = page
        self.user_input = page.locator('input#username')
        self.password_input = page.locator('input#password')
        self.login_submit_btn = page.locator('button#login-submit')

    def login(self, user, password):
        self.user_input.fill(user)
        self.login_submit_btn.click()
        self.password_input.fill(password)
        self.login_submit_btn.click()
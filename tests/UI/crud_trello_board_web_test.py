import re, pytest, os, uuid

from playwright.sync_api import expect
from src.pages.board import BoardPage
from src.pages.home import HomePage
from src.pages.login import LoginPage
from src.pages.components.header import HeaderComponent
from src.pages.components.workspace_nav import WorkspaceNavComponent

page = None
board = None
home = None
header = None
login = None
workspace = None
board_name = str(uuid.uuid4())
updated_board_name = str(uuid.uuid4())

@pytest.fixture(scope='function', autouse=True)
def before_each_after_each(playwright):
    global page
    global board
    global home
    global header
    global login
    global workspace
    # Before each
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    board = BoardPage(page)
    home = HomePage(page)
    header = HeaderComponent(page)
    login = LoginPage(page)
    workspace = WorkspaceNavComponent(page)

    home.goto()
    header.login_btn.click()
    login.login(
        os.getenv('USER_NAME'),
        os.getenv('PASSWORD')
    )
    yield
    # here can come an After each part

def test_should_create_update_and_delete_board_through_ui():
    home.section_header.wait_for()
    expect(home.section_header).to_contain_text('YOUR WORKSPACES')

    # create board
    home.create_new_board(board_name, '🌈')

    board.wait_for_page_loaded()
    workspace.nav.wait_for()

    expect(board.main_title).to_contain_text(board_name)

    #u pdate board
    board.update_board_name(updated_board_name)

    expect(board.main_title).to_contain_text(updated_board_name)

    # close board
    workspace.close_current_board()

    expect(board.close_board_message).to_contain_text(f'{updated_board_name} is closed.')

    # delete board
    board.delete_board()

    expect(home.section_header).to_contain_text('YOUR WORKSPACES')

    board_names = home.get_all_board_names()
    if (len(board_names) > 0):
        expect().not_to_contain_text(updated_board_name)

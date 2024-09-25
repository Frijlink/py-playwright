import uuid, os, pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('TRELLO_API_KEY')
API_TOKEN = os.getenv('TRELLO_API_TOKEN')
assert API_URL, 'API_URL is not set'
assert API_KEY, 'API_KEY is not set'
assert API_TOKEN, 'API_TOKEN is not set'

member_id = ''
organization_id = ''
board_id = ''
board_name = str(uuid.uuid4())
updated_board_name = str(uuid.uuid4())
background_colour = 'purple'
updated_background_colour = 'blue'
visibility = 'org'
updated_visibility = 'private'

@pytest.fixture(scope='session')
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        'Accept': 'application/json',
    }
    request_context = playwright.request.new_context(
        base_url=API_URL, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope='session', autouse=True)
def delete_boards_after_test(
    api_request_context: APIRequestContext,
) -> Generator[None, None, None]:
    global member_id
    global organization_id
    # Before all
    member_id = api_request_context.get(
        f'/1/tokens/{API_TOKEN}?key={API_KEY}&token={API_TOKEN}').json()['idMember']
    organization_id = api_request_context.get(
        f'/1/members/{member_id}/organizations?key={API_KEY}&token={API_TOKEN}').json()[0]['id']
    yield
    # After all
    boards = api_request_context.get(
        f'/1/members/me/boards?key={API_KEY}&token={API_TOKEN}').json()
    for board in boards:
        id = board['id']
        delete_board = api_request_context.delete(
            f'/1/boards/{id}?key={API_KEY}&token={API_TOKEN}')
    assert delete_board.ok

def test_should_create_board_through_api(api_request_context: APIRequestContext) -> None:
    global board_id

    data = {
        'name': board_name,
        'key': API_KEY,
        'token': API_TOKEN,
        'prefs_background':  background_colour,
        'prefs_permissionLevel': visibility,
    }
    url = f'{API_URL}/1/boards/'
    response = api_request_context.post(url, params=data)
    assert response.ok

    response_body = response.json()
    assert response_body['idOrganization'] == organization_id
    assert response_body['name'] == board_name
    assert response_body['closed'] == False
    assert response_body['prefs']['background'] == background_colour
    assert response_body['prefs']['permissionLevel'] == visibility

    board_id = response_body['id']

def test_should_read_board_through_api(api_request_context: APIRequestContext) -> None:
    response = api_request_context.get(
        f'/1/boards/{board_id}?key={API_KEY}&token={API_TOKEN}')
    assert response.ok

    response_body = response.json()
    assert response_body['idOrganization'] == organization_id
    assert response_body['name'] == board_name
    assert response_body['closed'] == False
    assert response_body['prefs']['background'] == background_colour
    assert response_body['prefs']['permissionLevel'] == visibility

def test_should_update_board_through_api(api_request_context: APIRequestContext) -> None:
    data = {
        'name': updated_board_name,
        'key': API_KEY,
        'token': API_TOKEN,
        'prefs/background':  updated_background_colour,
        'prefs/permissionLevel': updated_visibility,
    }
    response = api_request_context.put(f'/1/boards/{board_id}', params=data)
    assert response.ok

    response_body = response.json()
    assert response_body['idOrganization'] == organization_id
    assert response_body['name'] == updated_board_name
    assert response_body['closed'] == False
    assert response_body['prefs']['background'] == updated_background_colour
    assert response_body['prefs']['permissionLevel'] == updated_visibility

def test_should_close_board_through_api(api_request_context: APIRequestContext) -> None:
    data = {
        'key': API_KEY,
        'token': API_TOKEN,
        'closed': 'true'
    }
    response = api_request_context.put(f'/1/boards/{board_id}', params=data)
    assert response.ok

    response = api_request_context.get(
        f'/1/boards/{board_id}?key={API_KEY}&token={API_TOKEN}')
    assert response.ok

    response_body = response.json()
    assert response_body['closed'] == True

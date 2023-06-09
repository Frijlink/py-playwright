import uuid
import os
from typing import Generator

import pytest
from playwright.sync_api import Playwright, APIRequestContext

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("TRELLO_API_KEY")
API_TOKEN = os.getenv("TRELLO_API_TOKEN")
assert API_URL, "API_URL is not set"
assert API_KEY, "API_KEY is not set"
assert API_TOKEN, "API_TOKEN is not set"

organization_id = ""


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    headers = {
        "Accept": "application/json",
    }
    request_context = playwright.request.new_context(
        base_url=API_URL, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session", autouse=True)
def delete_boards_after_test(
    api_request_context: APIRequestContext,
) -> Generator[None, None, None]:
    # Before all
    yield
    # After all
    boards = api_request_context.get(
        f"/1/members/me/boards?key={API_KEY}&token={API_TOKEN}").json()
    for board in boards:
        id = board["id"]
        delete_board = api_request_context.delete(
            f"/1/boards/{id}?key={API_KEY}&token={API_TOKEN}")
    assert delete_board.ok


def test_crud_trello_board_through_api(api_request_context: APIRequestContext) -> None:
    boardName = str(uuid.uuid4())
    updatedBoardName = str(uuid.uuid4())
    backgroundColour = "purple"
    updatedBackgroundColour = "pink"
    visibility = "org"
    updatedVisibility = "private"

    member_id = api_request_context.get(
        f"/1/tokens/{API_TOKEN}?key={API_KEY}&token={API_TOKEN}").json()["idMember"]
    organization_id = api_request_context.get(
        f"/1/members/{member_id}/organizations?key={API_KEY}&token={API_TOKEN}").json()[0]["id"]

    # Create board
    url = f"{API_URL}/1/boards/"
    response = api_request_context.post(url, params=create_create_body(
        boardName, API_KEY, API_TOKEN, backgroundColour, visibility))
    response_body = response.json()

    assert response.ok
    assert response_body["idOrganization"] == organization_id
    assert response_body["name"] == boardName
    assert response_body["closed"] == False
    assert response_body["prefs"]["background"] == backgroundColour
    assert response_body["prefs"]["permissionLevel"] == visibility


def create_create_body(name, api_key, api_token, colour, visibility):
    return {
        "name": name,
        "key": api_key,
        "token": api_token,
        "prefs_background":  colour,
        "prefs_permissionLevel": visibility,
    }

# py-playwright #
Playwright POC in Python

## Prerequisites ##

[Python 3](https://www.python.org/downloads/) installed

## How do I get set up? ##
- Install Playwright for python with `pip install pytest-playwright`
- Install the drivers with `playwright install`
- Set the necessary environment variables:

| Variable         | Content                |
|------------------|------------------------|
| BASE_URL         | http://trello.com      |
| API_URL          | https://api.trello.com |
| RETRIES          | 0                      |
| USER_NAME        |                        |
| PASSWORD         |                        |
| TRELLO_API_KEY   |                        |
| TRELLO_API_TOKEN |                        |


## How to run the tests ##

- run the tests with `pytest`
- if you want fancy logging, use `DEBUG=pw:api pytest -s`
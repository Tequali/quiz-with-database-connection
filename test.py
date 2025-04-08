import pytest
from src import DBHandler


@pytest.fixture
def test_db_handler():
    db_connection = DBHandler()
    return db_connection


def test_connect_to_db(test_db_handler):
    test_db_handler.connect_to_db()
    assert test_db_handler.db_connection
    assert test_db_handler.messenger
    assert test_db_handler.db_connection.cursor


def test_search_everything(test_db_handler):
    expected_result: list = []
    test_db_handler.connect_to_db()
    result = test_db_handler.fetch_question("yugioh", 0)
    test_db_handler.close_connection()
    print(result)
    assert expected_result == result
    assert type(result) is list


# test getting new ids
# test adding a question (needs a test db with mock maybe?)

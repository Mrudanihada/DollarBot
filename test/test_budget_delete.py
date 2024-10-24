import pytest
from unittest import mock
from budget_delete import run

# Mocking helper functions
mock_user_list = {
    "12345": {
        "budget": {
            "overall": 100,
            "category": {"food": 50, "transport": 20}
        }
    }
}

def test_run_user_does_not_exist():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "67890"  # User does not exist in mock_user_list

    with mock.patch('helper.read_json', return_value=mock_user_list):
        run(message, mock_bot)
        mock_bot.send_message.assert_called_once_with("67890", "You don't have budget data to delete.")

def test_run_user_exists_no_budget_data():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "12345"  # User exists but has no budget data

    # Update the mock_user_list to simulate no budget
    mock_user_list["12345"]["budget"] = {}

    with mock.patch('helper.read_json', return_value=mock_user_list):
        run(message, mock_bot)
        mock_bot.send_message.assert_called_once_with("12345", "No budget data to delete.")

def test_run_user_budget_deleted():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "12345"  # User exists and has budget data

    with mock.patch('helper.read_json', return_value=mock_user_list), \
         mock.patch('helper.write_json') as mock_write_json:
        
        run(message, mock_bot)

        # Check that the budget data has been reset
        assert mock_user_list["12345"]["budget"] == {"overall": None, "category": {}}
        mock_write_json.assert_called_once_with(mock_user_list)
        mock_bot.send_message.assert_called_once_with("12345", "Budget data deleted successfully.")

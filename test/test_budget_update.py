import pytest
from unittest import mock
from budget_update import run, set_budget_type, save_category_budget, save_overall_budget, set_category_budget_amount, set_overall_budget, set_category_budget
import helper

@pytest.fixture
def bot_mock():
    bot = mock.Mock()
    return bot

@pytest.fixture
def user_list_mock():
    return {
        "12345": {
            "budget": {
                "overall": None,
                "category": {}
            }
        }
    }

def test_run(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    
    with mock.patch('helper.read_json', return_value=user_list_mock):
        run(message, bot_mock)
        bot_mock.reply_to.assert_called_once()

def test_set_budget_type_overall(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "Overall"

    with mock.patch('helper.getBudgetTypes', return_value={"overall": "Overall", "category": "Category"}):
        set_budget_type(message, bot_mock, user_list_mock)
        assert "budget" in user_list_mock["12345"]

def test_set_category_budget(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"

    with mock.patch('helper.getSpendCategories', return_value=["Food", "Transport"]):
        set_category_budget(message, bot_mock, user_list_mock)
        bot_mock.reply_to.assert_called_once()

def test_save_overall_budget(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "1000"

    save_overall_budget(message, bot_mock, user_list_mock)
    assert user_list_mock["12345"]["budget"]["overall"] == 1000

def test_save_category_budget(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "500"
    
    category = "Food"
    
    save_category_budget(message, bot_mock, user_list_mock, category)
    assert user_list_mock["12345"]["budget"]["category"][category] == 500

def test_invalid_budget_type(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "InvalidType"

    with mock.patch('helper.getBudgetTypes', return_value={"overall": "Overall", "category": "Category"}):
        with pytest.raises(Exception):
            set_budget_type(message, bot_mock, user_list_mock)

def test_invalid_category(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "InvalidCategory"

    with mock.patch('helper.getSpendCategories', return_value=["Food", "Transport"]):
        set_category_budget_amount(message, bot_mock, user_list_mock)

    bot_mock.send_message.assert_called_once_with(message.chat.id, "Invalid category.", reply_markup=mock.ANY)

def test_exception_handling_in_save_category_budget(bot_mock, user_list_mock):
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = ""

    category = "Food"

    with mock.patch('helper.throw_exception') as mock_throw:
        save_category_budget(message, bot_mock, user_list_mock, category)
        mock_throw.assert_called_once()

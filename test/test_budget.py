from mock import ANY
import mock
from mock.mock import patch
from telebot import types
from code import budget





@patch("telebot.telebot")
def test_post_operation_selection_failing_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(budget, "helper")
    budget.helper.getBudgetOptions.return_value = {}

    message = create_message("hello from budget test run!")
    budget.post_operation_selection(message, mc)
    mc.send_message.assert_called_with(11, "Invalid", reply_markup=mock.ANY)



def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

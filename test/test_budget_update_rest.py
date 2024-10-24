from code import budget_update
from mock import ANY
from mock.mock import patch
from telebot import types



@patch("telebot.telebot")
def test_post_category_add(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    message = create_message("hello from testing!")
    budget_update.post_category_add(message, mc)

    mc.reply_to.assert_called_with(message, "Select Option", reply_markup=ANY)


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

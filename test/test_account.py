import os
import json
from mock.mock import patch
from telebot import types
from code import add
from code import account
from code import helper
from mock import ANY
from mock import Mock
import pdb
import pytest


dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'


@patch('telebot.telebot')
def test_run_reply_to(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    account.run(message, mc)
    assert (mc.reply_to.called)
    
@patch('telebot.telebot')
def test_run_register_next_step_handler(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc.register_next_step_handler.return_value = True
    message = create_message("hello from test run!")
    account.run(message, mc)
    assert (mc.reply_to.called)
    assert (mc.register_next_step_handler.called)

@patch('telebot.telebot')
@patch('code.account.add_account_record', Mock(return_value='sfs'))
@patch('code.helper.write_json', Mock(return_value=None))
def test_post_category_selection_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    message = create_message_category("hello from testing!", "Savings")
    account.post_category_selection(message, mc)
    assert (mc.send_message.called)

@patch('telebot.telebot')
def test_post_category_selection_noMatchingCategory(mock_telebot, mocker):
        with pytest.raises(Exception) as e_info:
            raise Exception('It failed')

        mc = mock_telebot.return_value
        mc.send_message.return_value = []
        mc.reply_to.return_value = True

        mocker.patch.object(add, 'helper')
        account.helper.getSpendCategories.return_value = None

        message = create_message_category("hello from testing!", "DummyCategory")
        add.post_category_selection(message, mc)
        assert str(e_info.value) == 'It failed'

@patch('telebot.telebot')
@patch('code.helper.getCommands', Mock(return_value=[]))
def test_post_category_selection_noMatchingCategory_Exception_ReplyToCalled(mock_telebot, mocker):
        with pytest.raises(Exception) as e_info:
            raise Exception('It failed')

        mc = mock_telebot.return_value
        mc.send_message.return_value = []
        mc.reply_to.return_value = True

        mocker.patch.object(add, 'helper')
        account.helper.getSpendCategories.return_value = None

        message = create_message_category("hello from testing!", "DummyCategory")
        add.post_category_selection(message, mc)
        assert str(e_info.value) == 'It failed'

        assert (mc.reply_to.called)

@patch('telebot.telebot')
@patch('code.helper.getCommands', Mock(return_value=[]))
def test_post_category_selection_noMatchingCategory_Exception_SendMessageCalled(mock_telebot, mocker):
        with pytest.raises(Exception) as e_info:
            raise Exception('It failed')

        mc = mock_telebot.return_value
        mc.send_message.return_value = []
        mc.reply_to.return_value = True

        mocker.patch.object(add, 'helper')
        account.helper.getSpendCategories.return_value = None

        message = create_message_category("hello from testing!", "DummyCategory")
        add.post_category_selection(message, mc)
        assert str(e_info.value) == 'It failed'

        assert (mc.reply_to.called)
        assert (mc.send_message.called)
        assert (mc.send_message.called)

def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

def create_message_category(text, category):
    params = {'messagebody': text, 'text': category}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "") 
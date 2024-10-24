import pytest
from unittest.mock import patch
from telebot import types
from datetime import datetime
from code import add


dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"

@patch("telebot.telebot")
@patch("add.helper.read_json")
def test_run(user_mock,mock_telebot):
    mc = mock_telebot.return_value
    user_mock.return_value = create_user_list()
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    add.run(message, mc)
    assert not mc.reply_to.called

@patch("telebot.telebot")
def test_post_category_selection_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    message = create_message("hello from testing!")
    user_list = create_user_list()
    paid_by = 'User1'
    owed_by = ['User1']
    add.post_category_selection(message, mc,owed_by,paid_by,user_list)
    assert mc.send_message.called

@patch("telebot.telebot")
def test_post_category_selection_noMatchingCategory(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = []
    mc.reply_to.return_value = True
    mocker.patch.object(add, "helper")
    user_list = create_user_list()
    paid_by = 'User1'
    owed_by = ['User1','User2']
    add.helper.getSpendCategories.return_value = None
    message = create_message("Food")
    add.post_category_selection(message, mc,owed_by,paid_by,user_list)
    assert mc.reply_to.called

@patch("telebot.telebot")
def test_post_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    user_list = create_user_list()
    paid_by = 'User1'
    owed_by = ['User1','User2']
    message = create_message("40")
    add.post_category_selection(message, mc,owed_by,paid_by,user_list)
    assert mc.send_message.called

@patch("telebot.telebot")
def test_post_amount_input_working_withdata(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat
    mocker.patch.object(add, "option")
    add.option.return_value = {11, "here"}
    user_list = create_user_list()
    paid_by = 'User1'
    owed_by = ['User1','User2']
    message = create_message("40")
    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food",owed_by,paid_by,user_list)
    assert mc.send_message.called

@patch("telebot.telebot")
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food",['User1','User2'],'User1',create_user_list())
    assert mc.reply_to.called

@patch("telebot.telebot")
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add, "helper")
    add.helper.validate_entered_amount.return_value = 10
    add.helper.write_json.return_value = True
    add.helper.getDateFormat.return_value = dateFormat
    add.helper.getTimeFormat.return_value = timeFormat
    mocker.patch.object(add, "option")
    add.option = {11, "here"}
    test_option = {}
    test_option[11] = "here"
    add.option = test_option
    message = create_message("hello from testing!")
    add.post_amount_input(message, mc, "Food",['User1','User2'],'User1',create_user_list())
    assert mc.send_message.called
    assert mc.send_message.called_with(11)

def test_add_user_record_nonworking(mocker):
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = {}
    addeduserrecord = add.add_user_record(create_user_list(), "record : test",'11',
                                          "{},{},{}".format('17-Oct-2023 13:23', 'Food', '40'),40,['User1','User2'],'User1')
    assert addeduserrecord

def test_add_user_record_working(mocker):
    MOCK_USER_DATA = create_user_list()
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = MOCK_USER_DATA
    addeduserrecord = add.add_user_record(create_user_list(), "record : test",'11',
                                          "{},{},{}".format('17-Oct-2023 13:23', 'Food', '40'),40,['User1','User2'],'User1')
    if len(MOCK_USER_DATA) + 1 == len(addeduserrecord):
        assert True

def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")

    message = types.Message(1, None, None, chat, "text", params, "")
    message.text = text
    return message

def create_user_list():
    return {'users': ['User1'], 
                  'owed': {'User1': 0}, 
                  'owing': {'User1': {}}, 
                  'data': [], 
                  'csv_data': [], 
                  'budget': {'overall': '0', 'category': {'Food': '0', 'Groceries': '0', 'Utilities': '0', 'Transport': '0', 'Shopping': '0', 'Miscellaneous': '0'}}, 
                  '11': {'users': ['User1', 'User1', 'User2', 'User3', 'User4'], 'owed': {'User1': 57.5, 'User2': 0, 'User3': 0, 'User4': 0}, 
                         'owing': {'User1': {}, 'User2': {'User1': 22.5}, 'User3': {'User1': 12.5}, 'User4': {'User1': 22.5}}, 
                        'data': ['17-Oct-2023 13:16,Utilities,20.0', '17-Oct-2023 13:23,Transport,50.0', '18-Oct-2023 23:54,Food,30.0'], 'csv_data': ['17-Oct-2023 13:16,Utilities,20.0,Sho,User1', '17-Oct-2023 13:23,Transport,50.0,Sho,Sakshi & Rutuja & Sho & User4', '18-Oct-2023 23:54,Food,30.0,Sho,Sakshi & Sho & User4'], 'budget': {'overall': '0', 'category': {'Food': '0', 'Groceries': '0', 'Utilities': '0', 'Transport': '0', 'Shopping': '0', 'Miscellaneous': '0'}}}}


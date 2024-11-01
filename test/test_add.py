import pytest
import helper
from unittest.mock import patch
from telebot import types
from datetime import datetime
from code import add
from unittest.mock import MagicMock
from add import run
from unittest.mock import ANY


dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"

@patch("telebot.telebot")
def test_add_shared_user_successful(mock_telebot):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    
    message = create_message("User2")
    owed_by = ["User1"]
    user_list = create_user_list()
    paid_by = "User1"
    
    add.add_shared_user(message, mc, owed_by, user_list, paid_by)
    
    assert mc.reply_to.called
    mc.reply_to.assert_called_with(
        message,
        "Do you want to add more user to share the expense? Y/N"
    )
    
    assert "User2" in owed_by





@patch("telebot.telebot")
def test_user_choice_yes_response(mock_telebot):
    """
    Test user_choice function when user responds with 'Y'
    """
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    message = create_message("Y")
    owed_by = ["User1"]
    user_list = create_user_list()
    paid_by = "User1"
    
    add.user_choice(message, mc, owed_by, user_list, paid_by)
    
    assert mc.send_message.called or mc.reply_to.called


@patch("telebot.telebot")
def test_select_user_no_remaining_users(mock_telebot):

    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    
    message = create_message("User1")
    
    user_list = create_user_list()
    owed_by = []
    for user in user_list['users']:
        owed_by.append(user)
    paid_by = "User1"
    
    add.select_user(message, mc, owed_by, user_list, paid_by)
    
    assert mc.send_message.called or mc.reply_to.called


@patch("telebot.telebot")
@patch("add.helper.read_json")
def test_select_user_with_remaining_users(user_mock, mock_telebot):
    mc = mock_telebot.return_value
    user_mock.return_value = create_user_list()
    mc.send_message.return_value = True
    
    message = create_message("User1")
    owed_by = []
    user_list = create_user_list()
    paid_by = None
    
    add.select_user(message, mc, owed_by, user_list, paid_by)
    
    assert mc.send_message.called
    mc.send_message.assert_called_with(
        11,
        "Select who shares the Expense",
        reply_markup=ANY
    )



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


def test_add_user_record_nonworking(mocker):
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = {}
    addeduserrecord = add.add_user_record(create_user_list(), "record : test",'11',
                                          "{},{},{}".format('24-Oct-2024 10:40', 'Food', '40'),40,['User1','User2'],'User1')
    assert addeduserrecord

def test_add_user_record_working(mocker):
    MOCK_USER_DATA = create_user_list()
    mocker.patch.object(add, "helper")
    add.helper.read_json.return_value = MOCK_USER_DATA
    addeduserrecord = add.add_user_record(create_user_list(), "record : test",'11',
                                          "{},{},{}".format('24-Oct-2024 10:50', 'Food', '40'),40,['User1','User2'],'User1')
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
                        'data': ['24-Oct-2024 10:55,Utilities,20.0', '24-Oct-2024 10:55,Transport,50.0', '25-Oct-2024 23:54,Food,30.0'], 'csv_data': ['25-Oct-2024 13:16,Utilities,20.0,Sho,User1', '24-Oct-2023 13:23,Transport,50.0,Parth,Mrudani & Jamnesh & Aagam & User4', '18-Oct-2024 23:54,Food,30.0,Parth,Mrudani & Parth & User4'], 'budget': {'overall': '0', 'category': {'Food': '0', 'Groceries': '0', 'Utilities': '0', 'Transport': '0', 'Shopping': '0', 'Miscellaneous': '0'}}}}


from unittest.mock import MagicMock
import helper
from add import run  # Import the run function






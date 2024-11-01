import os
import json
from mock import patch
from telebot import types
from code import estimate
import pytest
from datetime import datetime, timedelta

def create_sample_history(days_back=30, categories=None):
    if categories is None:
        categories = ["Food", "Transport", "Entertainment"]
    history = []
    base_date = datetime.now()
    for i in range(days_back):
        date = base_date - timedelta(days=i)
        date_str = date.strftime("%d-%b-%Y")
        for cat in categories:
            history.append(f"{date_str},${cat},{20+i}")
    return history


@patch("telebot.telebot")
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    estimate.run(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_no_data_available(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("/spendings")
    estimate.run(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_invalid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("luster")
    try:
        estimate.estimate_total(message, mc)
        assert False
    except Exception:
        assert True


@patch("telebot.telebot")
def test_valid_format(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next month")
    try:
        estimate.estimate_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_valid_format_day(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next day")
    try:
        estimate.estimate_total(message, mc)
        assert True
    except Exception:
        assert False


@patch("telebot.telebot")
def test_spending_estimate_working(mock_telebot, mocker):

    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next day")
    message.text = "Next day"
    estimate.estimate_total(message, mc)
    assert mc.send_message.called


@patch("telebot.telebot")
def test_spending_estimate_month(mock_telebot, mocker):

    MOCK_USER_DATA = test_read_json()
    mocker.patch.object(estimate, "helper")
    estimate.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
    estimate.helper.getSpendEstimateOptions.return_value = ["Next day", "Next month"]
    estimate.helper.getDateFormat.return_value = "%d-%b-%Y"
    estimate.helper.getMonthFormat.return_value = "%b-%Y"
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("Next month")
    message.text = "Next month"
    estimate.estimate_total(message, mc)
    assert mc.send_message.called


def create_message(text):
    params = {"messagebody": text}
    chat = types.User(11, False, "test")
    return types.Message(894127939, None, None, chat, "text", params, "")


def test_read_json():
    try:
        if not os.path.exists("./test/dummy_expense_record.json"):
            with open("./test/dummy_expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("./test/dummy_expense_record.json").st_size != 0:
            with open("./test/dummy_expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


@patch("telebot.telebot")
def test_calculate_estimate_empty_data(mock_telebot):
    result = estimate.calculate_estimate([], 1)
    assert result == ""

# 2. Test single category calculation
@patch("telebot.telebot")
def test_calculate_estimate_single_category(mock_telebot):
    history = ["01-Jan-2024,Food,10.50"]
    result = estimate.calculate_estimate(history, 1)
    assert "Food $10.5" in result

# 3. Test multiple categories same day
@patch("telebot.telebot")
def test_calculate_estimate_multiple_categories_same_day(mock_telebot):
    history = [
        "01-Jan-2024,Food,10.50",
        "01-Jan-2024,Transport,20.00"
    ]
    result = estimate.calculate_estimate(history, 1)
    assert "Food $10.5" in result
    assert "Transport $20.0" in result

# 4. Test data spanning multiple days
@patch("telebot.telebot")
def test_calculate_estimate_multiple_days(mock_telebot, mocker):
    history = [
        "01-Jan-2024,Food,10.50",
        "02-Jan-2024,Food,15.50"
    ]
    result = estimate.calculate_estimate(history, 30)
    assert "Food $390.0" in result  # (10.50 + 15.50)/2 * 30    

# 5. Test with decimal precision
@patch("telebot.telebot")
def test_calculate_estimate_decimal_precision(mock_telebot):
    history = ["01-Jan-2024,Food,10.537"]
    result = estimate.calculate_estimate(history, 1)
    assert "Food $10.54" in result    

# 7. Test large numbers
@patch("telebot.telebot")
def test_calculate_estimate_large_numbers(mock_telebot):
    history = ["01-Jan-2024,Investment,1000000.00"]
    result = estimate.calculate_estimate(history, 1)
    assert "Investment $1000000.0" in result  

# 8. Test zero values
@patch("telebot.telebot")
def test_calculate_estimate_zero_values(mock_telebot):
    history = ["01-Jan-2024,Food,0.00"]
    result = estimate.calculate_estimate(history, 1)
    assert "Food $0.0" in result    

# 9. Test multiple months of data
@patch("telebot.telebot")
def test_calculate_estimate_multiple_months(mock_telebot):
    history = create_sample_history(60)
    result = estimate.calculate_estimate(history, 30)
    assert len(result.split("\n")) > 1    

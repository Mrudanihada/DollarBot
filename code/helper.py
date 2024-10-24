"""

MIT License

Copyright (c) 2021 Dev Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import re
import json
import os
from datetime import datetime

from notify import notify
spend_categories = [
    "Food",
    "Groceries",
    "Utilities",
    "Transport",
    "Shopping",
    "Miscellaneous",
]
choices = ["Date", "Category", "Cost"]
spend_display_option = ["Day", "Month"]
spend_estimate_option = ["Next day", "Next month"]
update_options = {"continue": "Continue", "exit": "Exit"}

budget_options = {"add":"Add","update": "Update", "view": "View", "delete": "Delete"}

budget_types = {"overall": "Overall Budget", "category": "Category-Wise Budget"}

data_format = {"users":[],"owed":{},"owing":{},"data": [],"csv_data":[], 
    "budget": {"overall": '0', "category": {"Food": '0',
                                            "Groceries": '0',
                                            "Utilities": '0',
                                            "Transport": '0',
                                            "Shopping": '0',
                                            "Miscellaneous": '0'}
                }
}

# set of implemented commands and their description
commands = {
    "help": "Display the list of commands.",
    "pdf": "Save history as PDF.",
    "csv": "Save history as a cv file.",
    "add_user": "Add users to expense tracker",
    "delete_user":"Delete user from the registered users",
    "add": "This option is for adding your expenses \
       \n 1. It will give you the list of categories to choose from. \
       \n 2. You will be prompted to enter the amount corresponding to your spending \
       \n 3.The message will be prompted to notify the addition of your expense with the amount,date, time and category ",
    "add_category": "This option is for adding new category \
       \n 1. You will be prompted to enter a new category \
       \n 2.The message will be prompted to notify the addition of your category ",

    "display": "This option gives user a graphical representation(bar graph) of their expenditures \
        \n You will get an option to choose from day or month for better analysis of the expenses.",
    "estimate": "This option gives you the estimate of expenditure for the next day/month. It calcuates based on your recorded spendings",
    "history": "This option is to give you the detailed summary of your expenditure with Date, time ,category and amount. A quick lookup into your spendings",
    "delete": "This option is to Clear/Erase all your records",
    "delete_expense": "This option is to Clear/Erase individual record from expense history records.",
    "send_mail": "This option is to send mail of calculate owings",
    "edit": "This option helps you to go back and correct/update the missing details \
        \n 1. It will give you the list of your expenses you wish to edit \
        \n 2. It will let you change the specific field based on your requirements like amount/date/category",
    "budget": "This option is to set/update/delete the budget. \
        \n 1. The Add/update category is to set the new budget or update the existing budget \
        \n 2. The view category gives the detail if budget is exceeding or in limit with the difference amount \
        \n 3. The delete category allows to delete the budget and start afresh!  ",
}

dateFormat = "%d-%b-%Y"
timeFormat = "%H:%M"
monthFormat = "%b-%Y"

# === Documentation of helper.py ===

# function to load .json expense record data


def read_json():
    """
    read_json(): Function to load .json expense record data
    """
    try:
        if not os.path.exists("expense_record.json"):
            with open("expense_record.json", "w") as json_file:
                json_file.write("{}")
            return json.dumps("{}")
        elif os.stat("expense_record.json").st_size != 0:
            with open("expense_record.json") as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(user_list):
    """
    write_json(user_list): Stores data into the datastore of the bot.
    """
    try:
        with open("expense_record.json", "w") as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print("Sorry, the data file could not be found.")


# function to validate the entered amount
def validate_entered_amount(amount_entered):
    """
    validate_entered_amount(amount_entered): Takes 1 argument, amount_entered.
    It validates this amount's format to see if it has been correctly entered by the user.
    """
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match(
        "^[1-9][0-9]{0,14}$", amount_entered
    ):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0

def getUserHistory(chat_id):
    """
    getUserHistory(chat_id): Takes 1 argument chat_id and uses this to get the relevant user's historical data.
    """
    data = getUserData(chat_id)
    if data is not None:
        return data["data"]
    return None

#function to validate the entered time
def validate_time_format(time_str):
    # Use a regular expression to match the time format HH:MM
    time_pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'

    if re.match(time_pattern, time_str):
        return True
    else:
        return False

# function to validate the entered duration
def validate_entered_duration(duration_entered):
    if duration_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}", duration_entered):
        duration = int(duration_entered)
        if duration > 0:
            return str(duration)
    return 0

# function to get user history
def getUserHistory(chat_id):
    data = getUserData(chat_id)
    if data is not None:
        return data['data']
    return None

# function to get user data
def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if (str(chat_id) in user_list):
        return user_list[str(chat_id)]
    return None

# function to throw exception
def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, 'Oh no! ' + str(e))

# function to create a new user record
def createNewUserRecord():
    return data_format

# function to get overall budget
def getOverallBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['overall']

def getUserReminder(chat_id):
    data = getUserData(chat_id)
    if data is not None:
        return data['data']
    return None


# function to get category based budget
def getCategoryBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['category']

# function to get category by category
def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]

# function to can add budget
def canAddBudget(chatId):
    return (getOverallBudget(chatId) is None) and (getCategoryBudget(chatId) is None)

# function to check if overall budget available or not
def isOverallBudgetAvailable(chatId):
    return getOverallBudget(chatId) is not None

# function to check if category budget available or not
def isCategoryBudgetAvailable(chatId):
    return getCategoryBudget(chatId) is not None

# function to check if category budget by category available or not
def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None:
        return False
    return cat in data.keys()

# function to check if there's balance in a particular account type
def isBalanceAvailable(chat_id, cat):
    data = getUserData(chat_id)
    if data['balance'][cat] is None:
        return False
    else:
        return data['balance'][cat]

# function to get balance in a particular category account.
def get_account_balance(message, bot, cat):
    if isBalanceAvailable(message.chat.id, cat):
        return float(isBalanceAvailable(message.chat.id, cat))
    else:
        return 0

# function to get the current active account for expenses.
def get_account_type(message):
    data = getUserData(message.chat.id)
    if data['account']['Checking'] == "True":
        return 'Checking'
    else:
        return 'Savings'

# function to display balance in a particular category account.
def display_account_balance(message, bot, cat):
    chat_id = message.chat.id
    if get_account_balance(message, bot, cat) != 0:
        print("Balance in {} account is: {}.".format(cat, float(get_account_balance(message, bot, cat))))
    else:
        print("This Account category has no existing balance")

# function to display remaining budget
def display_remaining_budget(message, bot, cat):
    chat_id = message.chat.id
    if isOverallBudgetAvailable(chat_id):
        display_remaining_overall_budget(message, bot)
    elif isCategoryBudgetByCategoryAvailable(chat_id, cat):
        display_remaining_category_budget(message, bot, cat)

# function to display remaining overall budget
def display_remaining_overall_budget(message, bot):
    print('here')
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    print("here", remaining_budget)
    if remaining_budget >= 0:
        msg = '\nRemaining Overall Budget is $' + str(remaining_budget)
    else:
        msg = '\nBudget Exceded!\nExpenditure exceeds the budget by $' + str(remaining_budget)[1:]
    bot.send_message(chat_id, msg)

# function to calculate remaining overall budget
def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings(queryResult)

# function to calculate total spending
def calculate_total_spendings(queryResult):
    total = 0

    for row in queryResult:
        s = row.split(',')
        total = total + float(s[2])
    return total

# function to display remaining category budget
def display_remaining_category_budget(message, bot, cat):
    chat_id = message.chat.id
    remaining_budget = calculateRemainingCategoryBudget(chat_id, cat)
    if remaining_budget >= 0:
        msg = '\nRemaining Budget for ' + cat + ' is $' + str(remaining_budget)
    else:
        msg = '\nBudget for ' + cat + ' Exceded!\nExpenditure exceeds the budget by $' + str(abs(remaining_budget))
    bot.send_message(chat_id, msg)

# function to calculate remaining category based budget
def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)

# function to calculate total spending per category
def calculate_total_spendings_for_category(queryResult, cat):
    total = 0

    for row in queryResult:
        s = row.split(',')
        if cat == s[1]:
            total = total + float(s[2])
    return total

# function to get spending categories
def getSpendCategories():
    with open("categories.txt", "r") as tf:
        spend_categories = tf.read().split(',')
    return spend_categories

def getAccountCategories():
    return account_categories 

#function to get different currencies
def getCurrencies():
    with open("currencies.txt", "r") as tf:
        currencies = tf.read().split(',')
    return currencies

# function to get plot
def getplot():
    return plot

# function to display spend options
def getSpendDisplayOptions():
    return spend_display_option

# function to get spend estimations
def getSpendEstimateOptions():
    return spend_estimate_option

# function to fetch commands
def getCommands():
    return commands

# function to fetch date format
def getDateFormat():
    return dateFormat

# function to fetch time format
def getTimeFormat():
    return timeFormat

# function to fetch month format
def getMonthFormat():
    return monthFormat

# function to fetch choices
def getChoices():
    return choices

# function to fetch budget options
def getBudgetOptions():
    return budget_options

# function to fetch budget types
def getBudgetTypes():
    return budget_types

# function to update options
def getUpdateOptions():
    return update_options

# function to fetch category options
def getCategoryOptions():
    return category_options

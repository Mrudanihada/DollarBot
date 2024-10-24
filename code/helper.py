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

def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if str(chat_id) in user_list:
        return user_list[str(chat_id)]
    return None


def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, "Oh no! " + str(e))


def createNewUserRecord(message):
    user_lst = data_format
    if len(user_lst["users"]) == 0:
        user_lst["users"].insert(0,message.from_user.first_name)
        user_lst["owed"][message.from_user.first_name] = 0
        user_lst["owing"][message.from_user.first_name] = {}
    return user_lst


def getOverallBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    if 'budget' in data.keys():
        return data["budget"]["overall"]
    return None


def getCategoryBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    if 'budget' in data.keys():
        return data["budget"]["category"]
    return None



def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]


def canAddBudget(chatId):
    return (getOverallBudget(chatId) is None) and (getCategoryBudget(chatId) is None)


def isOverallBudgetAvailable(chatId):
    return getOverallBudget(chatId) is not None


def isCategoryBudgetAvailable(chatId):
    return getCategoryBudget(chatId) is not None


def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None:
        return False
    return cat in data.keys()

def calculate_owing(user_list,chat_id):
    owing_dict = {}
    users = user_list[str(chat_id)]["users"]
    for user in users:
        owing_dict[user] = {"owes" : [], "owing":[]}
        for k,v in user_list[str(chat_id)]["owing"][user].items():
            if k in owing_dict.keys():
                owing_dict[k]["owing"].append(str(user)+' owes '+str(k)+" an amout of "+"{:.2f}".format(v))
                owing_dict[user]["owes"].append(str(k)+' is owing from '+str(user)+" an amout of "+"{:.2f}".format(v))

            else:
                owing_dict[k] ={"owes" :[str(k)+' is owing from '+str(user)+" an amout of "+"{:.2f}".format(v)],"owing" :[str(user)+' owes '+str(k)+" an amout of "+"{:.2f}".format(v)]}

    return owing_dict


def display_remaining_budget(message, bot, cat):
    print("inside")
    chat_id = message.chat.id
    if isOverallBudgetAvailable(chat_id):
        display_remaining_overall_budget(message, bot)
    elif isCategoryBudgetByCategoryAvailable(chat_id, cat):
        display_remaining_category_budget(message, bot, cat)


def display_remaining_overall_budget(message, bot):
    print("here")
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    print("here", remaining_budget)
    if remaining_budget >= 0:
        msg = "\nRemaining Overall Budget is $" + str(remaining_budget)
    else:
        msg = (
            "\nBudget Exceded!\nExpenditure exceeds the budget by $" + str(remaining_budget)[1:]
        )
        # notify()
    bot.send_message(chat_id, msg)


def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings(queryResult)


def calculate_total_spendings(queryResult):
    total = 0

    for row in queryResult:
        s = row.split(",")
        total = total + float(s[2])
    return total

def calculate_owing(user_list,chat_id):
    owing_dict = {}
    users = user_list[str(chat_id)]["users"]
    for user in users:
        owing_dict[user] = {"owes" : [], "owing":[]}
        for k,v in user_list[str(chat_id)]["owing"][user].items():
            if k in owing_dict.keys():
                owing_dict[k]["owing"].append(str(user)+' owes '+str(k)+" an amout of "+"{:.2f}".format(v))
                owing_dict[user]["owes"].append(str(k)+' is owing from '+str(user)+" an amout of "+"{:.2f}".format(v))

            else:
                owing_dict[k] ={"owes" :[str(k)+' is owing from '+str(user)+" an amout of "+"{:.2f}".format(v)],"owing" :[str(user)+' owes '+str(k)+" an amout of "+"{:.2f}".format(v)]}

    return owing_dict




def display_remaining_category_budget(message, bot, cat):
    chat_id = message.chat.id
    remaining_budget = calculateRemainingCategoryBudget(chat_id, cat)
    if remaining_budget >= 0:
        msg = "\nRemaining Budget for " + cat + " is $" + str(remaining_budget)
    else:
        rem_amount = ""
        rem_amount = str(abs(remaining_budget))
        notify(chat_id, cat, rem_amount)
        msg = "\nRemaining Budget for " + cat + " is $" + str(remaining_budget)
    bot.send_message(chat_id, msg)


def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)


def calculate_total_spendings_for_category(queryResult, cat):
    total = 0

    for row in queryResult:
        s = row.split(",")
        if cat == s[1]:
            total = total + float(s[2])
    return total


def getSpendCategories():
    """
    getSpendCategories(): This functions returns the spend categories used in the bot. These are defined the same file.
    """
    return spend_categories


def getSpendDisplayOptions():
    """
    getSpendDisplayOptions(): This functions returns the spend display options used in the bot. These are defined the same file.
    """
    return spend_display_option

# function to fetch commands
def getCommands():
    return commands

def calculate_total_spendings(queryResult):
    total = 0

    for row in queryResult:
        s = row.split(",")
        total = total + float(s[2])
    return total

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

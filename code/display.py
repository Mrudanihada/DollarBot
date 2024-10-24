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

import time
import helper
import graphing
import logging
from telebot import types
from datetime import datetime

# === Documentation of display.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot
    which is the telegram bot object from the main code.py function.
    """
    user_list=helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!"
        )
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add("Display all expenses")
        markup.add("Display owings")
        m = bot.send_message(chat_id, "Select what to display",reply_markup=markup)
        bot.register_next_step_handler(m, display_choice, bot,user_list,chat_id)


def display_choice(message,bot,user_list,chat_id):
    chat_id = message.chat.id
    choice = message.text
    if choice == 'Display all expenses':
        display_expenses(message,bot)
    elif choice =='Display owings':
         display_owings(message,bot,user_list,chat_id)
    else:
        m = bot.send_message(chat_id, "Select correct choice")
        bot.register_next_step_handler(m, run, bot)

def display_owings(message,bot,user_list,chat_id):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = len(user_list[str(chat_id)]["users"])
        for c in user_list[str(chat_id)]["users"]:
                markup.add(c)
        m = bot.send_message(chat_id, "Select user who's owings you want to display",reply_markup=markup)
        bot.register_next_step_handler(m, select_user, bot,user_list,chat_id)

def select_user(message,bot,user_list,chat_id):
    chat_id = message.chat.id
    user = message.text
    owing_dictionary = helper.calculate_owing(user_list,chat_id)
    final_string = ''
    for owed in owing_dictionary[user]["owes"]:
            final_string+=str("\n "+owed)
    for owing in owing_dictionary[user]["owing"]:
            final_string+=str("\n "+owing)
    if final_string == '':
        final_string = str(user)+' owes or is owed nothing'
    m = bot.send_message(chat_id, final_string)

def display_expenses(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for mode in helper.getSpendDisplayOptions():
        markup.add(mode)
    # markup.add('Day', 'Month')
    msg = bot.reply_to(
        message,
        "Please select a category to see the total expense",
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, display_total, bot)

def display_total(message, bot):
    """
    display_total(message, bot): It takes 2 arguments for processing - message which is
    the message from the user, and bot which is the telegram bot object from the
    run(message, bot): function in the same file. This function loads the user's data using
    the helper file's getUserHistory(chat_id) method. After this, depending on the option user
    has chosen on the UI, it calls the calculate_spendings(queryResult): to process the queried
    data to return to the user after which it finally passes the data to the UI for the user to view.
    """
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception(
                'Sorry I can\'t show spendings for "{}"!'.format(DayWeekMonth)
            )

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")

        bot.send_message(chat_id, "Hold on! Calculating...")
        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, "typing")
        time.sleep(0.5)

        total_text = ""

        if DayWeekMonth == "Day":
            query = datetime.now().today().strftime(helper.getDateFormat())
            # query all that contains today's date
            queryResult = [
                value for index, value in enumerate(history) if str(query) in value
            ]
        elif DayWeekMonth == "Month":
            query = datetime.now().today().strftime(helper.getMonthFormat())
            # query all that contains today's date
            queryResult = [
                value for index, value in enumerate(history) if str(query) in value
            ]
        total_text = calculate_spendings(queryResult)
        print("###########",total_text)
        monthly_budget = helper.getCategoryBudget(chat_id)
        if monthly_budget == None:
            message = "Looks like you have not entered any category-wise budget yet. Please enter your budget and then try to display the expenses."
            bot.send_message(chat_id, message)

            display_text = ""
            commands = helper.getCommands()
            for (
            c
            ) in (
                commands
            ):  # generate help text out of the commands dictionary defined at the top
                display_text += "/" + c + ": "
                display_text += commands[c] + "\n"
            bot.send_message(chat_id, "Please select a menu option from below:")
            bot.send_message(chat_id, display_text)
        else:
            print("Print Total Spending", total_text)
            print("Print monthly budget", monthly_budget)

            spending_text = ""
            if len(total_text) == 0:
                spending_text = "You have no spendings for {}!".format(DayWeekMonth)
                bot.send_message(chat_id, spending_text)
            else:
                spending_text = "Here are your total spendings {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(
                    DayWeekMonth.lower(), total_text
                )
                graphing.visualize(total_text, monthly_budget)
                bot.send_photo(chat_id, photo=open("expenditure.png", "rb"))
                # os.remove('expenditure.png')
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))


def calculate_spendings(queryResult):
    """
    calculate_spendings(queryResult): Takes 1 argument for processing - queryResult
    which is the query result from the display total function in the same file.
    It parses the query result and turns it into a form suitable for display on the UI by the user.
    """
    total_dict = {}
    print("!!!!!!",queryResult)
    for row in queryResult:
        # date,cat,money
        s = row.split(",")
        # cat
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    return total_text



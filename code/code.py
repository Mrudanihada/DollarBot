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

import logging
import time
from datetime import datetime
import telebot
from jproperties import Properties
import helper
import edit
import history
import pdf
import display
import estimate
import delete
import add
import add_category
import delete_expense
import send_mail
import budget
import csvfile
import add_user
import delete_user

configs = Properties()

with open("user.properties", "rb") as read_prop:
    configs.load(read_prop)
user_list = helper.read_json()
api_token = str(configs.get("api_token").data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}

# === Documentation of code.py ===

# Define listener for requests by user


def listener(user_requests):
    """
    listener(user_requests): Takes 1 argument user_requests and logs all user
    interaction with the bot including all bot commands run and any other issue logs.
    """
    for req in user_requests:
        if req.content_type == "text":
            print(
                "{} name:{} chat_id:{} \nmessage: {}\n".format(
                    str(datetime.now()),
                    str(req.chat.first_name),
                    str(req.chat.id),
                    str(req.text),
                )
            )

    message = (
        ("Sorry, I can't understand messages yet :/\n"
         "I can only understand commands that start with /. \n\n"
         "Type /faq or /help if you are stuck.")
    )

    try:
        helper.read_json()
        global user_list
        chat_id = user_requests[0].chat.id

        if user_requests[0].text[0] != "/":
            bot.send_message(chat_id, message)
    except Exception:
        pass

bot.set_update_listener(listener)


@bot.message_handler(commands=["help"])
def help(m):

    helper.read_json()
    global user_list
    chat_id = m.chat.id

    message = "Here are the commands you can use: \n"
    commands = helper.getCommands()
    for c in commands:
        message += "/" + c + ", "
    message += "\nUse /menu for detailed instructions about these commands."
    bot.send_message(chat_id, message)


@bot.message_handler(commands=["faq"])
def faq(m):

    helper.read_json()
    global user_list
    chat_id = m.chat.id

    faq_message = (
        ('"What does this bot do?"\n'
         ">> DollarBot lets you manage your expenses so you can always stay on top of them! \n\n"
         '"How can I add an epxense?" \n'
         ">> Type /add_category, then add a category for the expense. \n\n"
         ">> Type /add_category, then select a category to type the expense. \n\n"
         '"Can I see history of my expenses?" \n'
         ">> Yes! Use /display to get a graphical display, or/history to view detailed summary.\n\n"
         '"I added an incorrect expense. How can I edit it?"\n'
         ">> Use /edit command. \n\n"
         '"Can I check if my expenses have exceeded budget?"\n'
         ">> Yes! Use /budget and then select the view category. \n\n")
    )
    bot.send_message(chat_id, faq_message)


# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=["start", "menu"])
def start_and_menu_command(m):
    """
    start_and_menu_command(m): Prints out the the main menu displaying the features that the
    bot offers and the corresponding commands to be run from the Telegram UI to use these features.
    Commands used to run this: commands=['start', 'menu']
    """
    global user_list
    user_list = helper.read_json()
    chat_id = m.chat.id
    print(user_list)
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord(m)



    # print('receieved start or menu command.')
    # text_into = "Welcome to the Dollar Bot!"

    text_intro = (
        ("Welcome to the Dollar Bot! \n"
         "DollarBot can track all your expenses with simple and easy to use commands :) \n"
         "Here is the complete menu. \n\n")
    )
    # "Type /faq or /help to get stated."

    commands = helper.getCommands()
    for (
        c
    ) in (
        commands
    ):  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# defines how the /new command has to be handled/processed
@bot.message_handler(commands=["add"])
def command_add(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add.run(message, bot)


@bot.message_handler(commands=["add_user"])
def command_add_user(message):
    add_user.register_people(message,bot,user_list)

@bot.message_handler(commands=["delete_user"])
def command_delete_user(message):
    # Call the delete_user function from the delete_user module
    registered_users=user_list[str(message.chat.id)]["users"]
    delete_user.delete_user(message, bot, user_list)

@bot.message_handler(commands=["add_category"])
def command_add_category(message):
    """
    command_add(message) Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls add.py to run to execute
    the add functionality. Commands used to run this: commands=['add']
    """
    add_category.run(message, bot)
# function to fetch expenditure history of the user


@bot.message_handler(commands=["pdf"])
def command_pdf(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls pdf.py to run to execute
    the add functionality. Commands used to run this: commands=['pdf']
    """
    pdf.run(message, bot)


@bot.message_handler(commands=["csv"])
def command_csv(message):
    """
    command_history(message): Takes 1 argument message which contains the message from
    the user along with the chat ID of the user chat. It then calls csv.py to run to execute
    the add functionality. Commands used to run this: commands=['csv']
    """
    csvfile.run(message, bot)


# function to display total expenditure
@bot.message_handler(commands=["display"])
def command_display(message):
    """
    command_display(message): Takes 1 argument message which contains the message from the user
    along with the chat ID of the user chat. It then calls display.py to run to execute
    the add functionality.
    Commands used to run this: commands=['display']
    """
    display.run(message, bot)


# The main function
def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == '__main__':
    reminder_thread = threading.Thread(target=reminder_checker)
    reminder_thread.daemon = True
    reminder_thread.start()

    main()

import helper
import logging
from telebot import types
from datetime import datetime


option = {}


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It pop ups a menu on the bot asking the user to choose their expense category,
    after which control is given to post_category_selection(message, bot) for further proccessing.
    It takes 2 arguments for processing - message which is the message from the user,
    and bot which is the telegram bot object from the main code.py function.
    """
    user_list=helper.read_json()
    chat_id = message.chat.id
    owed_by =[]
    # option.pop(chat_id, None)  # remove temp choice

    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord(message)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = len(user_list[str(chat_id)]["users"])
    for c in user_list[str(chat_id)]["users"]:
        markup.add(c)
    m = bot.send_message(chat_id, "Select who paid for the Expense",reply_markup=markup)
    bot.register_next_step_handler(m, select_user, bot,owed_by,user_list,None)


def select_user(message,bot,owed_by,user_list,paid_by):
    chat_id = message.chat.id
    text_m = message.text
    remaining_users = [item for item in user_list[str(chat_id)]["users"] if item not in owed_by]
    if len(remaining_users)==0:
        post_append_spend(message,bot,owed_by,user_list,paid_by)
    else:
        if text_m in user_list[str(chat_id)]["users"]:
            paid_by = text_m
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2

        for c in remaining_users:
            markup.add(c)
        m = bot.send_message(chat_id, "Select who shares the Expense",reply_markup=markup)
        bot.register_next_step_handler(m, add_shared_user, bot,owed_by,user_list,paid_by)

def add_shared_user(message,bot,owed_by,user_list,paid_by):
    chat_id = message.chat.id
    user = message.text
    if user in user_list[str(chat_id)]["users"]:
        owed_by.append(user)
    else:
        pass
    choice = bot.reply_to(message, "Do you want to add more user to share the expense? Y/N")
    bot.register_next_step_handler(choice, user_choice, bot, owed_by,user_list,paid_by)
    
def user_choice(message, bot,owed_by, user_list,paid_by):
    Choice = message.text
    if Choice == "Y" or Choice == 'y':
        select_user(message,bot,owed_by,user_list,paid_by)
    elif Choice == "N" or Choice == 'n':
        post_append_spend(message,bot,owed_by,user_list,paid_by)



def post_append_spend(message, bot,owed_by,user_list,paid_by):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    m = bot.send_message(chat_id, "Select a category")
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, "Select Category", reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot,owed_by,paid_by,user_list)


def post_category_selection(message, bot,owed_by,paid_by,user_list):
    """
    post_category_selection(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot object
    from the run(message, bot): function in the add.py file. It requests the user 
    to enter the amount they have spent on the expense category chosen and then passes
    control to post_amount_input(message, bot): for further processing.
    """
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(
                chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                'Sorry I don\'t recognise this category "{}"!'.format(selected_category)
            )

        option[chat_id] = selected_category
        message = bot.send_message(
            chat_id,
            "How much did you spend on {}? \n(Enter numeric values only)".format(
                str(option[chat_id])
            ),
        )
        bot.register_next_step_handler(
            message, post_amount_input, bot, selected_category,owed_by,paid_by,user_list
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no! " + str(e))
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


def post_amount_input(message, bot, selected_category,owed_by,paid_by,user_list):
    """
    post_amount_input(message, bot): It takes 2 arguments for processing -
    message which is the message from the user, and bot which is the telegram bot
    object from the post_category_selection(message, bot): function in the add.py file.
    It takes the amount entered by the user, validates it with helper.validate() and then
    calls add_user_record to store it.
    """
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")

        date_of_entry = datetime.today().strftime(
            helper.getDateFormat() + " " + helper.getTimeFormat()
        )

        date_str, category_str, amount_str = (
            str(date_of_entry),
            str(option[chat_id]),
            str(amount_value),
        )

        helper.write_json(
            add_user_record(
                user_list,message,chat_id, "{},{},{}".format(date_str, category_str, amount_str),amount_value,owed_by,paid_by
            )
        )

        bot.send_message(
            chat_id,
            "The following expenditure has been recorded: You have spent ${} for {} on {}".format(
                amount_str, category_str, date_str
            ),
        )
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oh no. " + str(e))


def add_user_record(user_list,message,chat_id, record_to_be_added,amount_value,owed_by, paid_by):
    """
    add_user_record(chat_id, record_to_be_added): Takes 2 arguments -
    chat_id or the chat_id of the user's chat, and record_to_be_added which
    is the expense record to be added to the store. It then stores this expense record in the store.
    """
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord(message)
    owed_amount = float(amount_value)/len(set(owed_by))
    if "data" in user_list[str(chat_id)]:
        user_list[str(chat_id)]["data"].append(record_to_be_added)
    else:
        user_list[str(chat_id)]["data"] = [record_to_be_added]
    user_list[str(chat_id)]["owed"][paid_by] += float(amount_value)
    for user in set(owed_by):
        if user == paid_by:
            user_list[str(chat_id)]["owed"][paid_by] -= owed_amount
        elif paid_by in user_list[str(chat_id)]["owing"][user].keys():
            user_list[str(chat_id)]["owing"][user][paid_by] += owed_amount
        else:
            user_list[str(chat_id)]["owing"][user][paid_by] = owed_amount
    record_to_be_added+=",{},{}".format(paid_by,' & '.join(owed_by))
    if "csv_data" in user_list[str(chat_id)]:
        user_list[str(chat_id)]["csv_data"].append(record_to_be_added)
    else:
        user_list[str(chat_id)]["csv_data"] = [record_to_be_added]
    return user_list



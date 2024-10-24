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

import helper
from telebot import types
import history
# === Documentation of delete_expense.py ===

def run(m, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and
    bot which is the telegram bot object from the main code.py function. It gets the details
    for the expense to be edited from here and passes control onto edit2(m, bot): for further processing.
    """
    chat_id = m.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getUserHistory(chat_id):
        expense_data = c.split(",")
        str_date = "Date=" + expense_data[0]
        str_category = ",\t\tCategory=" + expense_data[1]
        str_amount = ",\t\tAmount=$" + expense_data[2]
        markup.add(str_date + str_category + str_amount)
    info = bot.reply_to(m, "Select expense to be deleted:", reply_markup=markup)
    bot.register_next_step_handler(info, select_category_to_be_deleted, bot)

def select_category_to_be_deleted(m, bot):
    info = m.text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    choice = bot.reply_to(m, "Are you sure you want to delete? Y/N")
    bot.register_next_step_handler(choice, delete_selected_data, bot, info)



def delete_selected_data(message, bot, selected_data):
    chat_id = message.chat.id
    user_history = helper.getUserHistory(chat_id)
    
    # Check if the user has selected any data
    if not selected_data:
        bot.send_message(chat_id, "No data selected for deletion.")
        return
    
    if str(message.text) == "Y" or str(message.text) == "y":
        # Initialize a list to keep track of the deleted records
        deleted_records = []
        
        components = selected_data.split(',')
        formatted_data = []

        for component in components:
            key, value = component.split('=')
            value = value.strip()

            # Check if the component is the "Amount" and remove the '$' sign
            if key.strip() == "Amount" and value.startswith("$"):
                value = value[1:]

            formatted_data.append(value)

        formatted_string = ','.join(formatted_data)
        
        # Compare each item in user_history with selected_data
        for expense_data in user_history:
            if formatted_string in expense_data:
                user_history.remove(expense_data)
                deleted_records.append(expense_data)
        
        # Update the user's history
        user_list = helper.read_json()
        user_list[str(chat_id)]["data"] = user_history
        helper.write_json(user_list)

        # Provide feedback to the user about the deleted records
        if deleted_records:
            bot.send_message(chat_id, "The following record has been deleted:")
             # Create a tabular representation of the data
            tabular_data = "```"
            tabular_data += "+-------------------+-------------------+-------------+\n"
            tabular_data += "|     DATE          |    CATEGORY       |   AMOUNT    |\n"
            tabular_data += "+-------------------+-------------------+-------------+\n"

            for line in deleted_records:
                rec = line.split(",")  # Assuming data is comma-separated
                if len(rec) == 3:
                    tabular_data += "| {:<15} | {:<17} | {:<11} |\n".format(rec[0], rec[1], rec[2])

            tabular_data += "+-------------------+-------------------+-------------+"
            tabular_data += "```"

            # Send the tabular data as a Markdown-formatted message
            bot.send_message(chat_id, tabular_data, parse_mode="Markdown")

            msg = bot.send_message(chat_id, "Do you want to see the updated expense history? Y/N")
            bot.register_next_step_handler(msg, show_updated_expense_history, bot)

        else:
            bot.send_message(chat_id, "No matching records found for deletion.")
    else:
        bot.send_message(chat_id, "No data deleted.")

def show_updated_expense_history(message, bot):
    if str(message.text) == "Y" or str(message.text) == "y":
        history.run(message, bot)

# function to delete a record
def deleteHistory(chat_id):
    """
    deleteHistory(chat_id): It takes 1 argument for processing - chat_id which is the
    chat_id of the user whose data is to deleted from the user list. It removes this entry from the user list.
    """
    global user_list
    if str(chat_id) in user_list:
        del user_list[str(chat_id)]
    return user_list


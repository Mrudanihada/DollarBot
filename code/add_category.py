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



option = {}

# === Documentation of add.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the add feature.
    It pop ups a menu on the bot asking the user to choose their expense category,
    after which control is given to post_category_selection(message, bot) for further proccessing.
    It takes 2 arguments for processing - message which is the message from the user,
    and bot which is the telegram bot object from the main code.py function.
    """
    helper.read_json()
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    message1 = bot.send_message(chat_id, "Please enter your category")
    bot.register_next_step_handler(message1, post_append_spend, bot)

def post_append_spend(message, bot):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    selected_category = message.text
    if selected_category.lower() in [x.lower() for x in helper.spend_categories]:
        bot.send_message(
            chat_id, "Category already exists", reply_markup=types.ReplyKeyboardRemove()
        )
        message1 = bot.send_message(chat_id, "Please enter a new category")
        bot.register_next_step_handler(message1, post_append_spend, bot)

    else:
        helper.spend_categories.append(selected_category)
        user_list = helper.read_json()
        user_list[str(chat_id)]["budget"]["category"][selected_category] = '0'
        helper.write_json(user_list)
        for c in helper.getSpendCategories():
            markup.add(c)
        bot.send_message(
                chat_id,
                "The following category has been added: {} ".format(
                    selected_category
                ),
            )

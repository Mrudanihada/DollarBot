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

from telebot import types
import logging
import helper

def run(message, bot):
    chat_id = message.chat.id
    user_list = helper.read_json()

    if str(chat_id) not in user_list:
        # Initialize the user's data with an empty budget dictionary
        user_list[str(chat_id)] = {"budget": {"overall": None, "category": {}}}

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    budget_types = helper.getBudgetTypes()
    markup.row_width = 2
    for btype in budget_types.values():
        markup.add(btype)
    msg = bot.reply_to(message, "Select Budget Type", reply_markup=markup)
    bot.register_next_step_handler(msg, set_budget_type, bot, user_list)

def set_budget_type(message, bot, user_list):
    try:
        chat_id = message.chat.id
        budget_type = message.text
        options = helper.getBudgetTypes()
        
        if budget_type not in options.values():
            bot.send_message(chat_id, "Invalid", reply_markup=types.ReplyKeyboardRemove())
            raise Exception('Sorry I don\'t recognise this budget type "{}"!'.format(budget_type))

        if budget_type == options["overall"]:
            set_overall_budget(message, bot, user_list)
        elif budget_type == options["category"]:
            set_category_budget(message, bot, user_list)
    
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def set_overall_budget(message, bot, user_list):
    chat_id = message.chat.id

    if str(chat_id) not in user_list:
        bot.send_message(chat_id, "You don't have budget data to set.")
        return
    
    try:
        msg = bot.reply_to(message, "Enter the Overall Budget", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, save_overall_budget, bot, user_list)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def save_overall_budget(message, bot, user_list):
    chat_id = message.chat.id
    overall_budget = message.text

    if not overall_budget:
        bot.send_message(chat_id, "Budget not set. Please enter a valid budget.")
        return

    if str(chat_id) not in user_list:
        bot.send_message(chat_id, "You don't have budget data to set.")
        return

    try:
        # Ensure the 'budget' dictionary exists
        if "budget" not in user_list[str(chat_id)]:
            user_list[str(chat_id)]["budget"] = {"overall": None, "category": {}}
        
        # Set the overall budget in the user's data
        user_list[str(chat_id)]["budget"]["overall"] = float(overall_budget)

        helper.write_json(user_list)

        bot.send_message(chat_id, f"Overall Budget set to ${str(overall_budget)}")
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def set_category_budget(message, bot, user_list):
    chat_id = message.chat.id

    if str(chat_id) not in user_list:
        bot.send_message(chat_id, "You don't have budget data to set.")
        return
    
    try:
        categories = helper.getSpendCategories()
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add(*categories)
        msg = bot.reply_to(message, "Select a Category for Budget", reply_markup=markup)
        bot.register_next_step_handler(msg, set_category_budget_amount, bot, user_list)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def set_category_budget_amount(message, bot, user_list):
    chat_id = message.chat.id
    category = message.text

    if category not in helper.getSpendCategories():
        bot.send_message(chat_id, "Invalid category.", reply_markup=types.ReplyKeyboardRemove())
        return
    
    try:
        msg = bot.reply_to(message, f"Enter Budget for {category}", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, save_category_budget, bot, user_list, category)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

def save_category_budget(message, bot, user_list, category):
    chat_id = message.chat.id
    category_budget = message.text

    if not category_budget:
        bot.send_message(chat_id, "Budget not set. Please enter a valid budget.")
        return

    if str(chat_id) not in user_list:
        bot.send_message(chat_id, "You don't have budget data to set.")
        return

    try:
        # Ensure the 'budget' dictionary exists
        if "budget" not in user_list[str(chat_id)]:
            user_list[str(chat_id)]["budget"] = {"overall": None, "category": {}}
        
        # Ensure the category budget dictionary exists
        if "category" not in user_list[str(chat_id)]["budget"]:
            user_list[str(chat_id)]["budget"]["category"] = {}
        
        # Set the category budget in the user's data
        user_list[str(chat_id)]["budget"]["category"][category] = float(category_budget)

        helper.write_json(user_list)

        bot.send_message(chat_id, f"Budget for {category} set to ${str(category_budget)}")
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

import helper
from telebot import types

# Initialize a dictionary to store registered users
registered_users = {}

def delete_user(message, bot, user_list):
    chat_id = message.chat.id
    user_dict = user_list.get(str(chat_id), {})
    
    if not user_dict or "users" not in user_dict:
        bot.send_message(chat_id, "No users are registered for deletion.")
        return
    
    # Get the list of all users from user_list
    all_users = user_dict.get("users", [])
    
    # Create a custom keyboard to let the user choose which user to delete
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for user in all_users:
        markup.add(user)
    
    msg = bot.send_message(chat_id, "Select the user you want to delete:", reply_markup=markup)
    bot.register_next_step_handler(msg, confirm_delete, bot, user_list)

def confirm_delete(message, bot, user_list):
    chat_id = message.chat.id
    user_name = message.text
    
    user_dict = user_list.get(str(chat_id), {})
    
    if "users" in user_dict and user_name in user_dict["users"]:
        user_dict["users"].remove(user_name)
        user_dict["owed"].pop(user_name, None)
        user_dict["owing"].pop(user_name, None)
        
        helper.write_json(user_list)
        
        bot.send_message(chat_id, f"{user_name} has been deleted successfully.")
        
        if not user_dict["users"]:
            bot.send_message(chat_id, "No users are registered after deletion.")
        else:
            bot.send_message(chat_id, "Updated list of registered users:\n" + '\n '.join(user_dict["users"]))
    else:
        bot.send_message(chat_id, f"{user_name} is not registered.")
    
    # Remove the custom keyboard
    # markup = types.ReplyKeyboardRemove(selective=False)
    # bot.send_message(chat_id, "Keyboard hidden. You can now use other commands.", reply_markup=markup)

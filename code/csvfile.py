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
import logging
from matplotlib import pyplot as plt
from telebot import types
import csv

# === Documentation of pdf.py ===


def run(message, bot):
    try:
        user_list=helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        print('User-history--> ',user_history)
        if user_history != None:
            data = user_list[str(chat_id)]['csv_data']
            message = "Alright. I just created a csv file of your expense history!"
            bot.send_message(chat_id, message)
            csv_file = 'expense_report.csv'
            # Open the CSV file for writing
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)

                # Write the header row
                writer.writerow(['Date', 'Category', 'Amount', 'Payer', 'Participants'])

                # Write the data from the list
                for item in data:
                    parts = item.split(',')
                    writer.writerow(parts)
            bot.send_document(chat_id, open("expense_report.csv", "rb"))
            print("CSV generated successfully.")
            #issue 15 - modified the format of pdf document - start
            
        
        #Issue 3 - added the else condition - start
        else:
            message = "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf."
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
        #Issue 3 - added the else condition - end

    except Exception as e:
        logging.exception(str(e))
        bot.send_message(message, "Oops!" + str(e))



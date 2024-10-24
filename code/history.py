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
import csv
from io import StringIO
# === Documentation of history.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the delete feature.
    It takes 2 arguments for processing - message which is the message from the user, and bot which
    is the telegram bot object from the main code.py function. It calls helper.py to get the user's
    historical data and based on whether there is data available, it either prints an error message or
    displays the user's historical data.
    """

    try:
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)

        if user_history is None:
            raise Exception("Sorry! No spending records found!")

        if len(user_history) == 0:
            bot.send_message(chat_id, "Sorry! No spending records found!")
        else:
            # Create a tabular representation of the data
            tabular_data = "```"
            tabular_data += "+-------------------+-------------------+-------------+\n"
            tabular_data += "|     DATE          |    CATEGORY       |   AMOUNT    |\n"
            tabular_data += "+-------------------+-------------------+-------------+\n"

            for line in user_history:
                rec = line.split(",")  # Assuming data is comma-separated
                if len(rec) == 3:
                    tabular_data += "| {:<15} | {:<17} | {:<11} |\n".format(rec[0], rec[1], rec[2])

            tabular_data += "+-------------------+-------------------+-------------+"
            tabular_data += "```"

            # Send the tabular data as a Markdown-formatted message
            bot.send_message(chat_id, tabular_data, parse_mode="Markdown")

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops! " + str(e))


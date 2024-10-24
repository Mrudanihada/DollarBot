'''
This pdf.py file contains code for generating pdfs for total expenses and for tracking who owes whom how much.
'''

import helper
import logging
from matplotlib import pyplot as plt
from telebot import types

#Issue 15 - Added tabulate and fpdf libraries
from tabulate import tabulate
from fpdf import FPDF

#Issue 23 - Added Tabula library
#import tabula

#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

#Issue - 33

# === Documentation of pdf.py ===


def run(message, bot):
    """
    run(message, bot): This is the main function used to implement the pdf save feature.
    """
    try:
        helper.read_json()
        chat_id = message.chat.id

        user_list = helper.read_json()
        #print('User-history--> ',user_history)
        print('User_list', user_list)

         #Issue 23 - add two pdf types - start

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #markup.row_width = 2
        markup.add("PDF for Total Expenses - Category wise", "PDF showing who owes whom how much")
        msg = bot.send_message(chat_id, "Which kind of PDF do you want to generate?", reply_markup=markup)

        user_history = helper.getUserHistory(chat_id)

        bot.register_next_step_handler(msg, pdfGeneration, bot,user_list, user_history)
        #Issue 23 - add two pdf types - end

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))

def pdfGeneration(message, bot, user_list, user_history):
        chat_id = message.chat.id
        choice = message.text

        if choice == 'PDF for Total Expenses - Category wise':        
            #Issue 3 - added the if condition - start
            if user_history != None:
            #Issue 3 - added the if condition - end
                message = "Alright. I just created a pdf of your expense history!"
                bot.send_message(chat_id, message)
                fig = plt.figure()
                ax = fig.add_subplot(1, 1, 1)
                top = 0.8
                if len(user_history) == 0:
                    plt.text(
                        0.1,
                        top,
                        "No record found!",
                        horizontalalignment="left",
                        verticalalignment="center",
                        transform=ax.transAxes,
                        fontsize=20,
                    )

                #issue 15 - modified the format of pdf document - start
                table_data = [entry.split(',') for entry in user_history]

                # Create a PDF document
                pdf = FPDF()
                pdf.add_page()

                # Set font
                pdf.set_font("helvetica", size=12)

                # Define the table columns
                columns = ["Date & Time", "Category", "Amount"]

                # Create a table and set its properties
                pdf.set_fill_color(135, 206, 235)  # Light blue
                pdf.set_font(family="helvetica",style="B")
                pdf.cell(0, 10, "Expense Report", ln=1, align="C", fill=True)
                pdf.set_fill_color(255, 255, 255)  # White
                pdf.ln()
                pdf.ln()
                # Add table headers
                pdf.set_font("helvetica", size=12, style="B")
                for col in columns:
                    pdf.cell(64, 10, col, border=1, align="C", fill=True)
                pdf.ln()

                # Add table data
                pdf.set_font("helvetica", size=10)
                for row in table_data:
                    for item in row:
                        pdf.cell(64, 10, item, border=1, align="C", fill=True)
                    pdf.ln()

                # Save the PDF
                pdf.output("expense_report.pdf")
                bot.send_document(chat_id, open("expense_report.pdf", "rb"))
                print("PDF generated successfully.")
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
        #Issue 23 - added code for generating pdf showing who owes whom how much
        elif choice == 'PDF showing who owes whom how much':
            message = "Alright. I just created a pdf of your expense history!"
            bot.send_message(chat_id, message)

            if user_history != None:
                pdf = FPDF()
                pdf.add_page()

                pdf.set_font("Arial", size=12)
                pdf.set_fill_color(135, 206, 235)  # Light blue
                pdf.set_font(family="Arial",style="B")
                pdf.cell(0, 10, "Expense Report", ln=1, align="C", fill=True)
                pdf.set_fill_color(255, 255, 255)  # White
                pdf.ln()
                pdf.ln()

                pdf.set_font("helvetica", size=12, style="B")
                pdf.cell(50, 10, "User", border=1, align="C", fill=True)
                pdf.cell(50, 10, "Gets back", border=1, align="C", fill=True)
                pdf.cell(50, 10, "Gives to", border=1, align="C", fill=True)
                pdf.cell(40, 10, "Gives Amount", border=1, align="C", fill=True)
                #pdf.cell(40, 10, "Data", border=1)
                pdf.ln()

                pdf.set_font("helvetica", size=12)
                for user, details in user_list.items():
                    #print('User! ', user)
                    #print('details! ', details)
                    for i, user_name in enumerate(details["users"]):
                        #amounts = ''
                        pdf.cell(50, 10, user_name, border=1, align="C", fill=True)
                        pdf.cell(50, 10, str(round(details["owed"][user_name], 2)), border=1, align="C", fill=True)
                        pdf.cell(50, 10, ', '.join(details["owing"][user_name].keys()), border=1, align="C", fill=True)
                        if details["owing"][user_name].values() != []:
                            pdf.cell(40, 10, ', '.join([str(round(x,2)) for x in details["owing"][user_name].values()]), border=1, align="C", fill=True)
                        else:
                            pdf.cell(40, 10, "None", border=1, align="C", fill=True)
                        pdf.ln()

                pdf.output("OwingTable.pdf")
                bot.send_document(chat_id, open("OwingTable.pdf", "rb"))
                print("PDF table created successfully.")

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

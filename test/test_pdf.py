import unittest
from unittest.mock import patch, MagicMock
from main import run, pdfGeneration  # Assuming this function is in a file called main.py

class TestPDFGeneration(unittest.TestCase):

    @patch("helper.read_json")
    @patch("helper.getUserHistory")
    def test_run_with_valid_user_history(self, mock_getUserHistory, mock_read_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789

        # Mocking user history and user list
        mock_read_json.return_value = {
            "123456789": {
                "csv_data": [
                    "2023-10-21,Groceries,50.00,John,Doe & Jane",
                    "2023-10-22,Transport,15.00,Jane,John & Doe"
                ],
                "users": ["John", "Jane"],
                "owed": {"John": 20, "Jane": 30},
                "owing": {"John": {"Jane": 20}, "Jane": {"John": 10}},
            }
        }
        mock_getUserHistory.return_value = ["2023-10-21,Groceries,50.00", "2023-10-22,Transport,15.00"]

        # Run the `run` function
        run(message, bot)

        # Verify that bot prompts the user with the PDF options
        bot.send_message.assert_called_once_with(123456789, "Which kind of PDF do you want to generate?")

        # Ensure the next step handler is registered for PDF generation
        bot.register_next_step_handler.assert_called()

    @patch("helper.read_json")
    @patch("helper.getUserHistory")
    def test_run_with_no_user_history(self, mock_getUserHistory, mock_read_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789

        # Mocking no user history
        mock_getUserHistory.return_value = None
        mock_read_json.return_value = {}

        # Run the `run` function
        run(message, bot)

        # Verify that the bot sends a message indicating no data and presents commands
        bot.send_message.assert_any_call(123456789, "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf.")

    @patch("helper.getCommands")
    def test_pdf_generation_expense_category(self, mock_getCommands):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789
        message.text = "PDF for Total Expenses - Category wise"

        user_list = {
            "123456789": {
                "users": ["John", "Jane"],
                "owed": {"John": 20, "Jane": 30},
                "owing": {"John": {"Jane": 20}, "Jane": {"John": 10}},
            }
        }
        user_history = ["2023-10-21,Groceries,50.00", "2023-10-22,Transport,15.00"]

        # Mock the plot and PDF generation
        with patch("matplotlib.pyplot.figure"), patch("fpdf.FPDF.output"), patch("builtins.open", new_callable=unittest.mock.mock_open):
            pdfGeneration(message, bot, user_list, user_history)

            # Verify that the bot sends the message
            bot.send_message.assert_called_once_with(123456789, "Alright. I just created a pdf of your expense history!")

            # Verify the bot sends the generated PDF document
            bot.send_document.assert_called()

    @patch("helper.getCommands")
    def test_pdf_generation_owing_table(self, mock_getCommands):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789
        message.text = "PDF showing who owes whom how much"

        user_list = {
            "123456789": {
                "users": ["John", "Jane"],
                "owed": {"John": 20, "Jane": 30},
                "owing": {"John": {"Jane": 20}, "Jane": {"John": 10}},
            }
        }
        user_history = ["2023-10-21,Groceries,50.00", "2023-10-22,Transport,15.00"]

        # Mock the PDF generation
        with patch("fpdf.FPDF.output"), patch("builtins.open", new_callable=unittest.mock.mock_open):
            pdfGeneration(message, bot, user_list, user_history)

            # Verify that the bot sends the message
            bot.send_message.assert_called_once_with(123456789, "Alright. I just created a pdf of your expense history!")

            # Verify the bot sends the generated PDF document
            bot.send_document.assert_called()

    def test_pdf_generation_invalid_choice(self):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789
        message.text = "Invalid Choice"

        user_list = {}
        user_history = None

        # Run the `pdfGeneration` function with an invalid choice
        pdfGeneration(message, bot, user_list, user_history)

        # Ensure that no PDF is generated and an error message is sent
        bot.send_message.assert_any_call(123456789, "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf.")


if __name__ == "__main__":
    unittest.main()

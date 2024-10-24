import unittest
from unittest.mock import MagicMock, patch
from main import run  # Assuming this function is in a file called main.py
import csv

class TestRunFunction(unittest.TestCase):

    @patch("helper.read_json")
    @patch("helper.getUserHistory")
    @patch("helper.getCommands")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    @patch("csv.writer")
    def test_run_with_user_history(self, mock_csv_writer, mock_open, mock_getCommands, mock_getUserHistory, mock_read_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789

        # Mocking user history and data
        mock_read_json.return_value = {
            "123456789": {
                "csv_data": [
                    "2023-10-21,Groceries,50.00,John,Doe & Jane",
                    "2023-10-22,Transport,15.00,Jane,John & Doe"
                ]
            }
        }
        mock_getUserHistory.return_value = True

        # Run the function
        run(message, bot)

        # Verify that the message is sent to the bot
        bot.send_message.assert_any_call(123456789, "Alright. I just created a csv file of your expense history!")

        # Verify that the CSV file is written correctly
        mock_open.assert_called_once_with('expense_report.csv', 'w', newline='')
        mock_csv_writer.return_value.writerow.assert_any_call(['Date', 'Category', 'Amount', 'Payer', 'Participants'])
        mock_csv_writer.return_value.writerow.assert_any_call(['2023-10-21', 'Groceries', '50.00', 'John', 'Doe & Jane'])
        mock_csv_writer.return_value.writerow.assert_any_call(['2023-10-22', 'Transport', '15.00', 'Jane', 'John & Doe'])

        # Verify that the CSV document is sent to the bot
        bot.send_document.assert_called_once()

    @patch("helper.read_json")
    @patch("helper.getUserHistory")
    @patch("helper.getCommands")
    def test_run_without_user_history(self, mock_getCommands, mock_getUserHistory, mock_read_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789

        # Mock user history to None
        mock_getUserHistory.return_value = None

        # Mocking commands list
        mock_getCommands.return_value = {
            "start": "Start using the bot",
            "add": "Add a new expense",
            "history": "View your expense history"
        }

        # Run the function
        run(message, bot)

        # Verify that the appropriate message is sent for no user history
        bot.send_message.assert_any_call(123456789, "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf.")
        bot.send_message.assert_any_call(123456789, "Please select a menu option from below:")
        bot.send_message.assert_any_call(123456789, "/start: Start using the bot\n/add: Add a new expense\n/history: View your expense history\n")

    @patch("helper.read_json")
    @patch("helper.getUserHistory")
    def test_run_with_exception(self, mock_getUserHistory, mock_read_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = 123456789

        # Simulate an exception in the code
        mock_getUserHistory.side_effect = Exception("Something went wrong")

        # Run the function
        run(message, bot)

        # Verify that the bot sends the exception message
        bot.send_message.assert_called_with(message, "Oops!Something went wrong")


if __name__ == "__main__":
    unittest.main()

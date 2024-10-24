import unittest
from unittest.mock import MagicMock, patch
import csvfile
import helper
from telebot import TeleBot

class TestCsvFile(unittest.TestCase):

    def setUp(self):
        # Mock the bot and message
        self.bot = MagicMock(spec=TeleBot)
        self.message = MagicMock()
        self.message.chat.id = 12345
        self.user_list = {
            str(self.message.chat.id): {
                'csv_data': [
                    '2024-10-12,Food,50,John,2',
                    '2024-10-13,Travel,100,Jane,1'
                ]
            }
        }

    @patch('helper.read_json')
    @patch('helper.getUserHistory')
    @patch('csvfile.csv.writer')
    @patch('builtins.open', new_callable=MagicMock)
    def test_run_with_user_history(self, mock_open, mock_csv_writer, mock_get_user_history, mock_read_json):
        # Set up mock functions
        mock_read_json.return_value = self.user_list
        mock_get_user_history.return_value = self.user_list[str(self.message.chat.id)]['csv_data']

        # Set up the mock writer
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Simulate opening the file and writing to it
        mock_open.return_value.__enter__.return_value = mock_writer

        # Run the function
        csvfile.run(self.message, self.bot)

        # Assert that the bot sends the expected message
        self.bot.send_message.assert_any_call(self.message.chat.id, "Alright. I just created a csv file of your expense history!")

        # Check if the bot sends the CSV file
        mock_open.assert_called_once_with("expense_report.csv", "w", newline='')
        self.bot.send_document.assert_called_once_with(self.message.chat.id, open("expense_report.csv", "rb"))

    @patch('helper.read_json')
    @patch('helper.getUserHistory')
    def test_run_without_user_history(self, mock_get_user_history, mock_read_json):
        # Set up mock functions
        mock_read_json.return_value = self.user_list
        mock_get_user_history.return_value = None  # Simulate no user history

        # Run the function
        csvfile.run(self.message, self.bot)

        # Assert that the bot sends the "no data" message
        self.bot.send_message.assert_any_call(self.message.chat.id, "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf.")

    @patch('helper.read_json')
    @patch('helper.getUserHistory')
    @patch('csvfile.csv.writer')
    @patch('builtins.open', new_callable=MagicMock)
    def test_csv_content(self, mock_open, mock_csv_writer, mock_get_user_history, mock_read_json):
        # Set up mocks
        mock_read_json.return_value = self.user_list
        mock_get_user_history.return_value = self.user_list[str(self.message.chat.id)]['csv_data']
        
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Simulate opening the file and writing to it
        mock_open.return_value.__enter__.return_value = mock_writer

        # Run the function
        csvfile.run(self.message, self.bot)

        # Check if the correct data is written to the CSV
        expected_calls = [
            (['Date', 'Category', 'Amount', 'Payer', 'Participants'],),
            (['2024-10-12', 'Food', '50', 'John', '2'],),
            (['2024-10-13', 'Travel', '100', 'Jane', '1'],)
        ]
        mock_writer.writerow.assert_has_calls(expected_calls, any_order=False)

if __name__ == '__main__':
    unittest.main()

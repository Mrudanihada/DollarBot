import unittest
from unittest.mock import MagicMock
import pdf
import helper

class TestPDFGeneration(unittest.TestCase):
    
    def setUp(self):
        # Mock the bot instance
        self.bot = MagicMock()
        self.message = MagicMock()
        self.message.chat.id = 12345  # Mock chat ID

    def test_no_user_history(self):
        # Simulate no user history
        helper.getUserHistory = MagicMock(return_value=None)
        
        # Mock the read_json to return an empty user list
        helper.read_json = MagicMock(return_value={})

        # Call the run function with the mocked bot
        pdf.run(self.message, self.bot)

        # Check if the bot sent the correct message
        self.bot.send_message.assert_called_with(
            self.message.chat.id,
            "Looks like you have not entered any data yet. Please enter some data and then try creating a pdf."
        )

    def test_pdf_generation_owing(self):
        # Setup user history
        user_history = ['Sample entry']
        helper.getUserHistory = MagicMock(return_value=user_history)
        
        # Mock the user list
        user_list = {
            12345: {
                'users': ['Alice', 'Bob'],
                'owed': {'Alice': 50.0, 'Bob': 0.0},
                'owing': {'Alice': {'Bob': 50.0}, 'Bob': {}}
            }
        }
        # Mock the helper function to return the user list
        helper.read_json = MagicMock(return_value=user_list)
        
        # Mock the next step handler call
        self.message.text = "PDF showing who owes whom how much"
        
        # Call the pdfGeneration function directly to test
        pdf.pdfGeneration(self.message, self.bot, user_list, user_history)

        # Assert that a PDF document was sent
        self.bot.send_document.assert_called_once()  # Check if send_document was called once

    def test_pdf_generation_total_expenses(self):
        # Setup user history
        user_history = ['Sample entry']
        helper.getUserHistory = MagicMock(return_value=user_history)
        
        # Mock the user list
        user_list = {
            12345: {
                'users': ['Alice', 'Bob'],
                'owed': {'Alice': 50.0, 'Bob': 0.0},
                'owing': {'Alice': {'Bob': 50.0}, 'Bob': {}}
            }
        }
        # Mock the helper function to return the user list
        helper.read_json = MagicMock(return_value=user_list)
        
        # Mock the next step handler call
        self.message.text = "PDF for Total Expenses - Category wise"
        
        # Call the pdfGeneration function directly to test
        pdf.pdfGeneration(self.message, self.bot, user_list, user_history)

        # Assert that a PDF document was sent
        self.bot.send_document.assert_called_once()  # Check if send_document was called once

if __name__ == "__main__":
    unittest.main()

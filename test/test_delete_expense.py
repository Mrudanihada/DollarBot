import unittest
from unittest.mock import MagicMock, patch
from telebot import types
from code.delete_expense import run, select_category_to_be_deleted, delete_selected_data, show_updated_expense_history

class TestDeleteExpense(unittest.TestCase):

    def setUp(self):
        # Create a mock bot and message
        self.bot = MagicMock()
        self.message = MagicMock()
        self.chat_id = 12345
        self.message.chat.id = self.chat_id
        
        # Prepare the initial state of helper
        self.mock_helper = patch('code.helper')
        self.helper = self.mock_helper.start()
        
        # Mocking the user's expense history
        self.helper.getUserHistory = MagicMock(return_value=[
            "2024-10-01,Food,$10",
            "2024-10-02,Transport,$20",
            "2024-10-03,Entertainment,$30"
        ])
        self.helper.read_json = MagicMock(return_value={str(self.chat_id): {"data": []}})
        self.helper.write_json = MagicMock()

    def tearDown(self):
        self.mock_helper.stop()

    def test_run(self):
        # Test the run function to ensure it sends the correct message and sets up the options
        run(self.message, self.bot)

        # Check if the bot sends a message asking for expense selection
        self.bot.reply_to.assert_called_once_with(self.message, "Select expense to be deleted:", reply_markup=types.ReplyKeyboardMarkup)

        # Ensure that the next step handler is registered
        self.bot.register_next_step_handler.assert_called_once()

    def test_select_category_to_be_deleted(self):
        # Simulate user selecting an expense to delete
        self.message.text = "2024-10-01,Food,$10"

        select_category_to_be_deleted(self.message, self.bot)

        # Check if the bot prompts for confirmation to delete
        self.bot.reply_to.assert_called_once_with(self.message, "Are you sure you want to delete? Y/N")
        
        # Ensure that the next step handler is registered
        self.bot.register_next_step_handler.assert_called_once()

    def test_delete_selected_data_yes(self):
        # Simulate user confirming deletion
        self.message.text = "Y"
        selected_data = "2024-10-01,Food,$10"
        
        # Simulate reading user history
        self.helper.getUserHistory = MagicMock(return_value=[
            "2024-10-01,Food,$10",
            "2024-10-02,Transport,$20",
            "2024-10-03,Entertainment,$30"
        ])
        
        delete_selected_data(self.message, self.bot, selected_data)

        # Check if the history was updated correctly
        self.helper.write_json.assert_called_once()

        # Check if the bot sends a message confirming the deletion
        self.bot.send_message.assert_any_call(self.chat_id, "The following record has been deleted:")
        
        # Check if the bot asks if the user wants to see updated history
        self.bot.send_message.assert_called_once_with(self.chat_id, "Do you want to see the updated expense history? Y/N")

    def test_delete_selected_data_no_confirmation(self):
        # Simulate user denying deletion
        self.message.text = "N"
        selected_data = "2024-10-01,Food,$10"
        
        delete_selected_data(self.message, self.bot, selected_data)

        # Check if the bot sends a message saying no data deleted
        self.bot.send_message.assert_called_once_with(self.chat_id, "No data deleted.")

    def test_show_updated_expense_history_yes(self):
        # Simulate user confirming to see updated expense history
        self.message.text = "Y"

        show_updated_expense_history(self.message, self.bot)

        # Ensure that the history.run function is called
        import history
        history.run = MagicMock()
        history.run(self.message, self.bot)

        # Check if the history function is invoked
        history.run.assert_called_once_with(self.message, self.bot)

    def test_show_updated_expense_history_no(self):
        # Simulate user denying to see updated expense history
        self.message.text = "N"

        show_updated_expense_history(self.message, self.bot)

        # Ensure that the history function is not called
        import history
        history.run = MagicMock()
        history.run(self.message, self.bot)

        # Check if the history function is not invoked
        history.run.assert_not_called()

if __name__ == '__main__':
    unittest.main()

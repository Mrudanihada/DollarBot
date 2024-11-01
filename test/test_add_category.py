import unittest
from unittest.mock import MagicMock, patch
#from code import helper
#from telebot import types
from code.add_category import run, post_append_spend

class TestAddCategory(unittest.TestCase):

    def setUp(self):
        # Create a mock bot and message
        self.bot = MagicMock()
        self.message = MagicMock()
        self.chat_id = 12345
        self.message.chat.id = self.chat_id
        
        # Prepare the initial state of helper
        self.mock_helper = patch('code.helper')
        self.helper = self.mock_helper.start()
        
        # Initialize spend categories and mock read_json to return a valid user list
        self.helper.spend_categories = ['Food', 'Transport']
        self.helper.read_json.return_value = {
            str(self.chat_id): {
                "budget": {
                    "category": {}
                }
            }
        }
        self.helper.write_json = MagicMock()

    def tearDown(self):
        self.mock_helper.stop()

    def test_run(self):
        # Test the run function
        run(self.message, self.bot)

        # Check if the bot sends a message asking for category
        self.bot.send_message.assert_called_once_with(self.chat_id, "Please enter your category")

        # Ensure that the next step handler is registered
        self.bot.register_next_step_handler.assert_called_once()


    def test_post_append_spend_new_category(self):
        # Simulate adding a new category
        self.message.text = 'Entertainment'

        # Call the function to add a new category
        post_append_spend(self.message, self.bot)

        # Check that the new category is added to spend_categories
        self.assertIn('Entertainment', self.helper.spend_categories)

        # Verify that write_json is called to save the updated user list
        self.helper.write_json.assert_called_once()

        # Check if the correct message is sent for a successful addition
        self.bot.send_message.assert_called_with(
            self.chat_id,
            "The following category has been added: Entertainment "
        )

    def test_post_append_spend_no_category(self):
        # Simulate user input without a category
        self.message.text = ''

        # Call post_append_spend with empty input
        post_append_spend(self.message, self.bot)

        # Assert that the bot asks for a new category again
        self.bot.send_message.assert_called_with(self.chat_id, "Please enter a new category")

if __name__ == '__main__':
    unittest.main()

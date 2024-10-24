import unittest
from unittest.mock import MagicMock, patch, ANY
from telebot import types
from code.delete_user import delete_user, confirm_delete

class TestDeleteUser(unittest.TestCase):

    def setUp(self):
        # Mock the bot and message
        self.bot = MagicMock()
        self.chat_id = 12345
        self.message = MagicMock()
        self.message.chat.id = self.chat_id
        self.user_list = {
            str(self.chat_id): {
                'users': ['Alice', 'Bob'],
                'owed': {},
                'owing': {}
            }
        }

    @patch('code.helper.write_json')
    def test_delete_existing_user(self, mock_write_json):
        # Simulate the user selecting to delete 'Alice'
        self.message.text = 'Alice'  # User selects 'Alice' for deletion
        
        # Call delete_user to initiate the deletion process
        delete_user(self.message, self.bot, self.user_list)

        # Verify the bot sends a message prompting to confirm deletion
        self.bot.send_message.assert_called_with(self.chat_id, "Select the user you want to delete:", reply_markup=ANY)

        # Simulate the next step handler confirming deletion
        next_msg = MagicMock()  # Create a new message mock for the next step
        next_msg.chat.id = self.chat_id
        next_msg.text = self.message.text  # Simulate confirming deletion for 'Alice'
        confirm_delete(next_msg, self.bot, self.user_list)

        # Assertions after deletion
        self.assertNotIn('Alice', self.user_list[str(self.chat_id)]['users'])  # Ensure 'Alice' is deleted
        self.assertIn('Bob', self.user_list[str(self.chat_id)]['users'])  # Ensure 'Bob' is still there
        self.bot.send_message.assert_any_call(self.chat_id, "Alice has been deleted successfully.")
        self.bot.send_message.assert_any_call(self.chat_id, "Updated list of registered users:\nBob")

        # Verify that the helper function to write JSON was called
        mock_write_json.assert_called_once_with(self.user_list)

    @patch('code.helper.write_json')
    def test_delete_non_existing_user(self, mock_write_json):
        # Simulate the user selecting to delete a non-existing user 'Charlie'
        self.message.text = 'Charlie'  # User selects 'Charlie' for deletion
        
        # Call delete_user to initiate the deletion process
        delete_user(self.message, self.bot, self.user_list)

        # Verify the bot sends a message prompting to confirm deletion
        self.bot.send_message.assert_called_with(self.chat_id, "Select the user you want to delete:", reply_markup=ANY)

        # Simulate the next step handler confirming deletion
        next_msg = MagicMock()  # Create a new message mock for next step
        next_msg.chat.id = self.chat_id
        next_msg.text = self.message.text  # Simulate confirming deletion for non-existing user
        confirm_delete(next_msg, self.bot, self.user_list)

        # Assertions for non-existing user
        self.bot.send_message.assert_called_with(self.chat_id, "Charlie is not registered.")
        self.assertEqual(self.user_list[str(self.chat_id)]['users'], ['Alice', 'Bob'])  # Users should remain unchanged
        # Ensure write_json was not called since no user was deleted
        mock_write_json.assert_not_called()

    @patch('code.helper.write_json')
    def test_delete_user_no_registered_users(self, mock_write_json):
        # Set up user_list without registered users
        self.user_list[str(self.chat_id)] = {'users': []}

        # Call delete_user to initiate the deletion process
        delete_user(self.message, self.bot, self.user_list)

        # Check for the message about no users registered
        self.bot.send_message.assert_called_with(self.chat_id, "No users are registered for deletion.")
        # Ensure write_json was not called since there are no users to delete
        mock_write_json.assert_not_called()

if __name__ == '__main__':
    unittest.main()

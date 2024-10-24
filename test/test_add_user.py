import unittest
from unittest.mock import MagicMock, patch
from telebot import types
import helper

# Mock data
mock_chat_id = 123456789
mock_user_list = {
    str(mock_chat_id): {
        "users": []
    }
}

class TestRegisterUser(unittest.TestCase):

    @patch("helper.createNewUserRecord")
    @patch("helper.write_json")
    def test_register_new_user_flow(self, mock_write_json, mock_createNewUserRecord):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = mock_chat_id
        mock_createNewUserRecord.return_value = {"users": []}

        # Step 1: Test register_people
        from main import register_people, registered_users
        register_people(message, bot, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "Enter the name of the person you want to register:")

        # Check that add_person is registered as the next handler
        bot.register_next_step_handler.assert_called()

        # Step 2: Test add_person (when name is unique)
        from main import add_person
        msg = MagicMock()
        msg.chat.id = mock_chat_id
        msg.text = "John Doe"
        registered_users[mock_chat_id] = []

        add_person(msg, bot, registered_users, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "John Doe has been registered successfully!")

        # Ensure John Doe is added to registered users
        self.assertIn("John Doe", registered_users[mock_chat_id])

        # Step 3: Test add_person (when name is already registered)
        bot.send_message.reset_mock()
        add_person(msg, bot, registered_users, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "John Doe is already registered.")

    def test_handle_registration_choice(self):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = mock_chat_id
        message.text = "Register Another Person"
        
        # Test when user chooses to register another person
        from main import handle_registration_choice, registered_users
        registered_users[mock_chat_id] = ["John Doe"]

        handle_registration_choice(message, bot, registered_users, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "Enter the name of the person you want to register:")

        # Test when user chooses to finish registration
        message.text = "Finish Registration"
        bot.send_message.reset_mock()

        handle_registration_choice(message, bot, registered_users, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "Registered Users:\nJohn Doe")
        self.assertIn("John Doe", mock_user_list[str(mock_chat_id)]["users"])

        # Test invalid choice
        message.text = "Invalid Choice"
        bot.send_message.reset_mock()

        handle_registration_choice(message, bot, registered_users, mock_user_list)
        bot.send_message.assert_called_with(mock_chat_id, "Invalid choice. Please select a valid option.")

    @patch("helper.write_json")
    def test_handle_finish_registration(self, mock_write_json):
        bot = MagicMock()
        message = MagicMock()
        message.chat.id = mock_chat_id
        message.text = "Finish Registration"
        from main import handle_registration_choice, registered_users

        registered_users[mock_chat_id] = ["John Doe", "Jane Doe"]

        handle_registration_choice(message, bot, registered_users, mock_user_list)

        # Check that users are stored properly in user_list
        self.assertIn("John Doe", mock_user_list[str(mock_chat_id)]["users"])
        self.assertIn("Jane Doe", mock_user_list[str(mock_chat_id)]["users"])

        # Check that helper.write_json is called to save the user list
        mock_write_json.assert_called_with(mock_user_list)

        # Check that registered users are displayed correctly
        bot.send_message.assert_called_with(mock_chat_id, "Registered Users:\nJohn Doe\nJane Doe")


if __name__ == "__main__":
    unittest.main()

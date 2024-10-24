import unittest
from unittest.mock import MagicMock
import add_user
import helper
from telebot import types

class TestAddUser(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()
        self.chat_id = 12345
        self.message = MagicMock()
        self.message.chat.id = self.chat_id
        self.message.text = "Test User"
        self.user_list = {}

    def test_register_people_new_user(self):
        # Simulate the behavior of a new user
        self.message.chat.id = self.chat_id
        self.user_list = {}
        
        helper.createNewUserRecord = MagicMock(return_value={"users": []})

        add_user.register_people(self.message, self.bot, self.user_list)

        # Test if user is added correctly
        self.assertIn(str(self.chat_id), self.user_list)
        self.assertEqual(self.user_list[str(self.chat_id)]["users"], [])

    def test_register_people_existing_user(self):
        # Simulate an existing user
        self.user_list[str(self.chat_id)] = {"users": ["Existing User"]}

        add_user.register_people(self.message, self.bot, self.user_list)

        # Check if the bot sends the correct message for entering the name
        self.bot.send_message.assert_called_once_with(self.chat_id, "Enter the name of the person you want to register:")

    def test_add_person_new_name(self):
        # Simulate adding a new person
        registered_users = {}
        self.user_list[str(self.chat_id)] = {"users": []}

        add_user.add_person(self.message, self.bot, registered_users, self.user_list)

        # Test if new user is added
        self.assertIn("Test User", self.user_list[str(self.chat_id)]["users"])
        self.bot.send_message.assert_called_with(self.chat_id, "Test User has been registered successfully!")

    def test_add_person_existing_name(self):
        # Simulate adding an existing person
        registered_users = {self.chat_id: ["Test User"]}
        self.user_list[str(self.chat_id)] = {"users": ["Test User"]}

        add_user.add_person(self.message, self.bot, registered_users, self.user_list)

        # Check if the bot sends the correct message
        self.bot.send_message.assert_called_with(self.chat_id, "Test User is already registered.")

    def test_handle_registration_choice_register_another(self):
        # Simulate choosing to register another person
        self.message.text = "Register Another Person"
        registered_users = {self.chat_id: ["User1"]}

        add_user.handle_registration_choice(self.message, self.bot, registered_users, self.user_list)

        # Check if the bot prompts for another person
        self.bot.send_message.assert_called_with(self.chat_id, "Enter the name of the person you want to register:")

    def test_handle_registration_choice_finish_registration(self):
        # Simulate finishing registration
        self.message.text = "Finish Registration"
        self.user_list[str(self.chat_id)] = {"users": ["User1"]}
        registered_users = {self.chat_id: ["User1"]}

        add_user.handle_registration_choice(self.message, self.bot, registered_users, self.user_list)

        # Check if the users are saved and message sent
        self.assertIn("User1", self.user_list[str(self.chat_id)]["users"])
        self.bot.send_message.assert_called_with(self.chat_id, "Registered Users:\nUser1")

if __name__ == '__main__':
    unittest.main()

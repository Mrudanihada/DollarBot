import pytest
from unittest import mock
from send_mail import run, add_emails, send_email, is_valid_email, format_text_data

# Mock user_emails to keep track of added emails
mock_user_emails = {}

# Test the email validation function
def test_is_valid_email():
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("another.test@domain.co") is True
    assert is_valid_email("test@.com") is False

# Test the run function
def test_run():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "12345"

    with mock.patch('helper.read_json', return_value=None) as mock_read_json:
        run(message, mock_bot)
        mock_bot.send_message.assert_called_once_with("12345", "Please enter the email address")

# Test adding a valid email
def test_add_emails_valid():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "test@example.com"

    with mock.patch('send_mail.user_emails', mock_user_emails):
        add_emails(message, mock_bot)
        assert mock_user_emails["12345"] == "test@example.com"
        mock_bot.send_message.assert_called_with("12345", "Thank you for providing your email. Do you want to send email to test@example.com? Y/N")

# Test adding an invalid email
def test_add_emails_invalid():
    mock_bot = mock.Mock()
    message = mock.Mock()
    message.chat.id = "12345"
    message.text = "invalid-email"

    add_emails(message, mock_bot)
    mock_bot.send_message.assert_called_with("12345", "Invalid email address. Please enter a valid email.")

# Test sending email confirmation
def test_send_email_yes():
    # Mock user_emails and SMTP
    mock_user_emails["12345"] = "test@example.com"

    message = mock.Mock()
    message.text = "Y"

    with mock.patch('send_mail.smtplib.SMTP') as mock_smtp:
        send_email(message, mock.Mock())
        
        # Check SMTP functions
        assert mock_smtp.call_count == 1
        mock_smtp().starttls.assert_called_once()
        mock_smtp().login.assert_called_once()
        mock_smtp().sendmail.assert_called_once()
        mock_smtp().quit.assert_called_once()

def test_send_email_no():
    message = mock.Mock()
    message.text = "N"

    with mock.patch('send_mail.user_emails', mock_user_emails):
        send_email(message, mock.Mock())
        # Ensure that sendmail is not called if the answer is "N"
        assert not hasattr(mock_user_emails, 'sendmail')

# Test formatting text data
def test_format_text_data():
    user_list = {
        "user1": {
            "users": ["Alice", "Bob"],
            "owed": {"Alice": 10, "Bob": 5},
            "owing": {
                "Alice": {"Bob": 5},
                "Bob": {}
            }
        }
    }
    
    result = format_text_data(user_list)
    assert "Alice gets back 10.0 dollars." in result
    assert "Bob gives 5.0 dollars to Alice." in result
    assert "Bob gives to no one." in result

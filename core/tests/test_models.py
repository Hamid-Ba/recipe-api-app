from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelsTest(TestCase):
    """Test Models"""

    def test_create_user_should_work_properly(self):
        email = "test@example.com"
        password = "test123"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_entered_email_should_be_in_right_format(self):
        emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["test2@Example.com", "test2@example.com"],
            ["Test3@EXAMPLE.com",'Test3@example.com'],
            ["TEST4@Example.com",'TEST4@example.com']
        ]

        for email ,normalized in emails:
            user = get_user_model().objects.create_user(email=email)
            self.assertEqual(user.email,normalized)
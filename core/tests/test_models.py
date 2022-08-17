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

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminTest(TestCase):
    """Test Admin Panel"""
    def setUp(self):
        self.client = Client()
        self.admin = get_user_model().objects.create_superuser(
            email = "admin@example.com",
            password = "password123"
        )
        self.client.force_login(self.admin)

        self.user = get_user_model().objects.create_user(
            email = "user@example.com",
            password = "password123",
            name = "User"
        )

    def test_user_list(self):
        """Test User List Should Work Properly"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
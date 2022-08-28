"""
Test Tag Endpoints
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag 

from recipe.serializers import TagSerializer

TAG_URL = reverse("recipe:tag-list")

def create_user(email='test@example.com', password='test'):
    """Create User Helper Function"""
    return get_user_model().objects.create_user(email,password)

def create_tag(user,name):
    """Create Tag Helper Function"""
    return Tag.objects.create(user=user,name=name)

class PublicTest(TestCase):
    """Test Not Authorized User"""

    def setUp(self):
        self.clent = APIClient()

    def test_user_should_be_authorized(self):
        """Test User should be authorized"""
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Test Authorized Functionality User Can Access To"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_user_can_access_to_tags_list(self):
        """Authenticated User Has Access To Tags List"""
        create_tag(self.user,'Desserte')
        create_tag(self.user,'Drink')

        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code , status.HTTP_200_OK)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags,many=True)

        self.assertEqual(res.data , serializer.data)

    def test_user_can_access_to_his_tags(self):
        """Authenticated User Can Access To his Tags List"""
        other_user = create_user("other_user@example.com")
        create_tag(other_user,'Desserte')
        tag = create_tag(self.user,'Drink')
    
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code , status.HTTP_200_OK)

        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['id'] , tag.id)
        self.assertEqual(res.data[0]['name'] , tag.name)
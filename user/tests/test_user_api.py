"""Test User Api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 

CREATE_USER_URL = reverse("user:create")

def create_user(**payLoad):
    """Shortcut Create User"""
    return get_user_model().objects.create_user(**payLoad)

class PublicTest(TestCase):
    """Test User Public Section"""
    def setUp(self):
        
        self.client = APIClient()

    def test_user_should_be_registered_properly(self):
        """User Registration API"""
        payload = {
            "email" : "test@example.com",
            "password" : "pass123456",
            "name" : "user test"
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)    

        created_user = get_user_model().objects.get(email=payload["email"])
        self.assertEqual(created_user.email , payload["email"])
        self.assertTrue(created_user.check_password(payload["password"]))
        self.assertNotIn("password",res.data)

    def test_user_email_does_not_exist(self):
        """User Email Must Be Unique"""
        payload = {
            "email" : "test1@example.com",
            "password" : "pass123456",
            "name" : "user test"
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_password_should_not_be_short(self):
        """User Password Should Not Be Short"""
        new_payload = {
            "email" : "test@example.com",
            "password" : "pw",
            "name" : "new user test"
        }

        res = self.client.post(CREATE_USER_URL,new_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.filter(email=new_payload["email"]).exists()
        self.assertFalse(user)
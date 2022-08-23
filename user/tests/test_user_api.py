"""Test User Api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 

CREATE_USER_URL = reverse("user:create")
TOKEN_USER_URL = reverse("user:token")
ME_USER_URL = reverse("user:me")

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

    def test_create_token_should_work_properly(self):
        """ Test Token Creation """
        payload = {
            'email' : "test@example.com",
            'password' : 'pass123456',
            'name' : 'test user'
        }

        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code , status.HTTP_200_OK)

    def test_wrong_password_should_not_authorize(self):
        """ Test Token Creation With Wrong Password """
        payload = {
            'email' : "test@example.com",
            'password' : 'pass123456',
        }

        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL,{'email' : payload["email"] , 'password' : "wrongpass"})

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blank_password_should_not_authorize(self):
        """ Test Token Creation With Blank Password """
        payload = {
            'email' : "test@example.com",
            'password' : 'pass123456',
        }

        create_user(**payload)
        res = self.client.post(TOKEN_USER_URL,{'email' : payload["email"] , 'password' : ""})

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test Retrieve Unauthorized """
        res = self.client.get(ME_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTest(TestCase):
    """Authorized User Test Cases"""
    def setUp(self):
        payload = {
            "email" : "test@example.com",
            "password" : "pass123456",
            "name" : "User Test"
        }

        self.client = APIClient()
        self.user = create_user(**payload)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_profile(self):
        """ Authorized User Profile """
        res = self.client.get(ME_USER_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data , {
            "email" : "test@example.com",
            "name" : "User Test",
        })

    def test_retrieve_user_me_with_post(self):
        """ Test If Method Is Post Type"""
        res = self.client.post(ME_USER_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test Update User Profile """
        new_info = {
            "name" : "new Name",
            "password" : "newPassword"
        }
        res = self.client.patch(ME_USER_URL,new_info)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(self.user.name , new_info["name"])
        self.assertTrue(self.user.check_password(new_info["password"]))
"""Test Recipe Api"""
import email
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 
from decimal import Decimal

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse("recipe:recipe")


def create_recipe(user,**new_defaults):
    """Helper Function for creating a Recipe"""
    defaults = {
        'title' : 'test recipe title',
        'time_minute' : 5,
        'desc' : 'test',
        'link' : 'https://test.recipe.com',
        'price' : Decimal("100.00"),
    }

    defaults.update(new_defaults)
    return Recipe.objects.create(user=user, **defaults)

class PublicRecipeTest(TestCase):
    """Test For Unauthorized User"""
    def setUp(self):
        self.client = APIClient()

    def test_unathurized_user(self):
        """Test if user is unauthorized"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code , status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeTest(TestCase):
    """Test For Authorized User"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="user@example.com", password="password")
        self.client.force_authenticate(user=self.user)

    def test_get_user_recipe(self):
        """test user recipe"""
        create_recipe(self.user)
        create_recipe(self.user)
        
        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes , many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipes_of_authenticated_user(self):
        """test the recipes which belong to authenticated user"""
        other_user = get_user_model().objects.create_user(email="other@example.com")

        create_recipe(other_user)
        create_recipe(self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data ,serializer.data)
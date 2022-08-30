"""
Test Ingredient EndPoints
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

def create_user(email='test@example.com', password='test'):
    """Create User Helper Function"""
    return get_user_model().objects.create_user(email,password)

def create_ingredient(user , name):
    """Create Ingredient Helper Function"""
    return Ingredient.objects.create(user=user,name=name)

class PublicTest(TestCase):
    """no authorize user has no access to the ingredient."""
    def setUp(self):
        self.client = APIClient()

    def test_no_public_endpoint(self):
        """there is no public endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTest(TestCase):
    """Private Test Cases"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_user_can_access_to_ingredient_list(self):
        """test user can access to an ingredient list"""
        create_ingredient(user=self.user,name="Egg")
        create_ingredient(user=self.user,name="Tomato")

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients,many=True)

        self.assertEqual(res.data,serializer.data)

    def test_user_can_access_to_his_ingredients(self):
        """User Can Access to his Ingredient"""
        other_user = create_user("other_user@example.com")
        create_ingredient(other_user,"Egg")
        ingredient = create_ingredient(self.user,"Tomato")

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        ingredient = Ingredient.objects.get(user=self.user)
        
        self.assertEqual(res.data[0]['id'] , ingredient.id)
        self.assertEqual(res.data[0]['name'] , ingredient.name)
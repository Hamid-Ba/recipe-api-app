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

def get_ingredient_url(ingredient_id):
    """Return Ingredient URL"""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])

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

    def test_update_ingredient_should_work_properly(self):
        """Test Update Ingredient should work correctly"""
        ingredient = create_ingredient(self.user,"Egg")

        payload = {"name" : "Potato"}

        url = get_ingredient_url(ingredient.id)
        res = self.client.patch(url,payload)

        ingredient.refresh_from_db()
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(ingredient.name,payload["name"])

    def test_delete_ingredient_should_work_properly(self):
        """Test Delete Ingredient should work correctly"""
        ingredient = create_ingredient(self.user,"Egg")

        url = get_ingredient_url(ingredient.id)
        res = self.client.delete(url)

        ingredients = Ingredient.objects.filter(user=self.user)

        self.assertEqual(res.status_code , status.HTTP_204_NO_CONTENT)
        self.assertNotIn(ingredient,ingredients)


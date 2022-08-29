"""Test Recipe Api"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status 
from decimal import Decimal

from core.models import Recipe, User , Tag
from recipe import serializers
import recipe
from recipe.serializers import (RecipeSerializer,RecipeDetailSerializer)

RECIPE_URL = reverse("recipe:recipe-list")

def get_recipe_detail_url(recipe_id):
    """Get Recipe By Id"""
    return reverse("recipe:recipe-detail",args=[recipe_id])

def create_tag(user,name):
    """Create Tag Helper Function"""
    return Tag.objects.create(user=user, name=name)

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

    def test_get_recipe_detail(self):
        """Test Getting recipe detail"""
        recipe = create_recipe(self.user)
        
        serializer = RecipeDetailSerializer(recipe)
        res = self.client.get(get_recipe_detail_url(recipe.id))

        self.assertEqual(res.status_code , status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_create_recipe_should_work_properly(self):
        """Test Recipe Creation Procces"""
        payload = {
            'title' : 'test recipe title',
            'time_minute' : 5,
            'desc' : 'test',
            'link' : 'https://test.recipe.com',
            'price' : Decimal("100.00"),
        }

        res = self.client.post(RECIPE_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        for (k, v) in payload.items():
            self.assertEqual(getattr(recipe,k), v)
        
        self.assertEqual(recipe.user , self.user)

    def test_create_recipe_via_tag(self):
        """Test Creating a new recipe via tags"""
        payload = {
            "title" : "Omlet",
            "time_minute" : 10,
            "desc" : "delicious dinner",
            "price" : Decimal("3.95"),
            "tags" : [
                {"name" : "Dinner"},
                {"name" : "Egg"}
            ]
        }
        res = self.client.post(RECIPE_URL, payload,format = "json")
        self.assertEqual(res.status_code , status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]

        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.tags.count() , 2)
        
        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tags(self):
        """Test Create Recipe with existing tags"""
        tag_1 = create_tag(self.user,"Dinner")
        
        payload = {
            "title" : "Omlet",
            "time_minute" : 10,
            "desc" : "delicious dinner",
            "price" : Decimal("3.95"),
            "tags" : [{"name" : "Dinner"} , {"name" : "Egg"}]
        }

        res = self.client.post(RECIPE_URL,payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.filter(user=self.user)[0]

        self.assertIn(tag_1,recipe.tags.all())

        for tag in payload['tags']:
            exists = recipe.tags.filter(name=tag['name'],user=self.user).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test Create Tag When Recipe Is Modified"""
        recipe = create_recipe(self.user)

        payload = {"tags": [{"name" : "Dinner"}]}

        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url,payload, format="json")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        tag = Tag.objects.filter(name="Dinner")
        self.assertEqual(tag.count(),1)
        tag = tag[0]
        self.assertIn(tag , recipe.tags.all())

    def test_assign_tag_to_recipe(self):
        """Test Assgin Tag To Recipe"""
        existed_tag = Tag.objects.create(user=self.user,name="Dinner")
        recipe = create_recipe(self.user)
        recipe.tags.add(existed_tag)
    
        assing_tag = Tag.objects.create(user=self.user,name="Lunch")
        payload = {"tags": [{"name" : "Lunch"}]}

        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url,payload,format="json")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

        self.assertIn(assing_tag, recipe.tags.all())
        self.assertNotIn(existed_tag , recipe.tags.all())

    def test_clear_recipe_tags(self):
        """Clear The Tag Of Recipe"""    
        recipe = create_recipe(self.user)
        tag_1 = create_tag(self.user,"Dinner")
        recipe.tags.add(tag_1)

        payload = {"tags":[]}

        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url,payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertNotIn(tag_1 , recipe.tags.all())
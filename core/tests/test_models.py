from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core.models import (Ingredient, Recipe , Tag)


def create_user(email="test@example.com") :
    """Create User Helper Function"""
    return get_user_model().objects.create_user(email)

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

    def test_user_email_have_to_be_required(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="")

    def test_create_superuser_should_work_properly(self):
        email = "test@example.com"
        password = "test123"
        user = get_user_model().objects.create_superuser(email=email, password=password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe_should_work_properly(self):
        """Test For Create Recipe"""
        user = get_user_model().objects.create_user(email="test@example.com")
        title = "Recipe Test"
        time_minute = 5
        price = Decimal(10.00)
        desc = "This is a test"
        link = "https://example.com/recipe/link"

        recipe = Recipe.objects.create(title=title,time_minute=time_minute, price=price, desc=desc, link=link,user=user)

        self.assertEqual(str(recipe) , title)
        self.assertEqual(recipe.time_minute , time_minute)
        self.assertEqual(recipe.price , price)
        self.assertEqual(recipe.desc , desc)
        self.assertEqual(recipe.link , link)
        self.assertEqual(recipe.user , user)

    def test_create_tag_should_work_properly(self):
        """Test Tag Creation Procces"""
        user = create_user()

        tag = Tag.objects.create(user=user,name="Desserte")

        self.assertEqual(tag.user , user)
        self.assertEqual(str(tag) , "Desserte")

    def test_create_ingredient_should_work_properly(self):
        """Test ingredient Model"""
        user = create_user()
        name = 'Egg'
        ingredient = Ingredient.objects.create(user=user,name=name)

        self.assertEqual(str(ingredient) , name)
        self.assertEqual(ingredient.user , user)
        
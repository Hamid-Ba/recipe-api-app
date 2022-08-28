"""
Recipe Mapping URLs
"""
from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include,
    )

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSets)
router.register('tags', views.TagViewSets)

app_name = "recipe"

urlpatterns = [
    path("",include(router.urls)),
]
"""
Recipe View
"""
from rest_framework import (viewsets,mixins)
from core.models import Ingredient, Recipe, Tag

from recipe.serializers import (IngredientSerializer, RecipeSerializer, RecipeDetailSerializer, TagSerializer)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RecipeViewSets(viewsets.ModelViewSet):
    """Recipe Viewset(Controller)"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Customize Recipe List"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Specify The Serializer class"""
        if self.action == "list":
            self.serializer_class = RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create Recipe For Specific User"""
        return serializer.save(user=self.request.user)

class TagViewSets(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Tag ViewSets"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

class IngredientViewSets(mixins.ListModelMixin
                        ,mixins.UpdateModelMixin
                        , viewsets.GenericViewSet):
    """Ingredient ViewSets"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

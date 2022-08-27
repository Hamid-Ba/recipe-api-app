from rest_framework import viewsets
from core.models import Recipe

from recipe.serializers import (RecipeSerializer, RecipeDetailSerializer)
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
        """Customize """
        return Recipe.objects.filter(user = self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.action == "list":
            self.serializer_class = RecipeSerializer

        return self.serializer_class
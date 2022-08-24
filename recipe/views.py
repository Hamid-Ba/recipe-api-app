from rest_framework import viewsets
from core.models import Recipe

from recipe.serializers import RecipeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RecipeViewSets(viewsets.ModelViewSet):
    """Recipe Viewset(Controller)"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(user = self.request.user).order_by("-id")
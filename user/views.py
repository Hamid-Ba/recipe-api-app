"""
User Views
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """ User View For Registration """
    serializer_class = UserSerializer

class AuthTokenView(ObtainAuthToken):
    """User Authorization View"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
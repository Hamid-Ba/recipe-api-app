"""
User Views
"""
from rest_framework import generics

from user.serializers import UserSerializer
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    """ User View For Registration """
    serializer_class = UserSerializer
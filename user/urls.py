"""
User URL
"""
from django.urls import path

from user.views import AuthTokenView, CreateUserView

app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view() , name = "create"),
    path("token/", AuthTokenView.as_view() , name = "token")
]
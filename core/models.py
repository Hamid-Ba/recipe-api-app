from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    """User Object Manager"""
    
    def create_user(self,email,password=None,**extra_fields):
        """Create a new user"""
        if not email: raise ValueError
        
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self,email,password=None,**extra_fields):
        """Create a superuser"""
        if not email: raise ValueError
        
        user = self.model(email=self.normalize_email(email), is_staff=True,is_superuser=True ,**extra_fields)
        user.set_password(password)
        user.save()
        
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """User Model"""

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
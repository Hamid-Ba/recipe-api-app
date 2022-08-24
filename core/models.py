from django.db import models
from django.conf import settings
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

class Recipe(models.Model):
    """Recipe Model"""

    title = models.CharField(max_length=225)
    time_minute = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits = 5)
    desc = models.TextField(blank=True)
    link = models.CharField(max_length=300,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) :
        return self.title
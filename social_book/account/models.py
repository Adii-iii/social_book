from django.db import models
from django.utils import timezone
import dateutil
from datetime import date
import datetime

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# from ...social_book import settings
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

# User = get_user_model()

User = settings.AUTH_USER_MODEL
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    # file_type = models.CharField(max_length=10)
    # file_path = models.CharField(max_length=200)
    file = models.FileField(upload_to='books/')
    # file_name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class BookUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    
    def generate_token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email")
        
        email = self.normalize_email(email)
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.deactivated = False
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    public_visibility = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=True)
    address = models.CharField(max_length=40, default="")
    phone_no = models.CharField(max_length=10)
    birthday = models.DateField(default=date.today)
    age = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=30, default="")

    # age = models.PositiveIntegerField(max_length=30, editable=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def get_age(self):
        if self.birthday:
            today = date.today()
            return (
                today.year
                - self.birthday.year
                - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            )
        return None

    def save(self, *args, **kwargs):
        self.age = self.get_age 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
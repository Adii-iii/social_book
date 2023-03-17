from django.db import models
from django.utils import timezone
import dateutil
from datetime import date
import datetime

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


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
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=40, default="")
    phone_no = models.CharField(max_length=10)
    birthday = models.DateField(default=date.today)
    age = models.IntegerField(null=True, blank=True)

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

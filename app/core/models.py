import uuid
import os
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.conf import settings


def recipe_image_file_path(instance, filename):
    '''return the correct file path for recipe image upload'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


class AuthUserManager(BaseUserManager):
    '''Auth manager for the AuthUser Model'''

    def create_user(self, email, password=None, **extra_field):
        '''create and return a new user'''
        if not email:
            raise ValueError("Email field is required!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        '''create and return a superuser'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AuthUserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    '''Recipe tag model'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        '''return string representation of tag model'''
        return self.name


class Ingredient(models.Model):
    '''recipe ingredient model'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='ingredients')

    def __str__(self):
        '''return string representation of ingredient model'''
        return self.name


class Recipe(models.Model):
    '''recipe model'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        '''return string representation of recipe model'''
        return self.title

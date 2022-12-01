from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.conf import settings


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user'
    )

    def __str__(self):
        '''return string representation of tag model'''
        return self.name

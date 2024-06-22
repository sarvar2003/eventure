from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin#
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError
from django.db import models

from typing import Any

# Create your models here.


class UserManager(BaseUserManager):

    """Manager class for custom user model"""

    def create_user(self, email, first_name, last_name, password, **kwargs: Any) -> Any:
        
        """Creates a new user with email validation"""

        if not email: 
            raise ValidationError(_('Email is required please enter your email'))

        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password, **kwagrs: Any) -> Any:

        """Creates super user"""

        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password)

        user.is_staff = True

        user.is_verified = True

        user.is_active = True

        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    """Base User Model"""

    first_name = models.CharField(_("First Name"), max_length=250)
    last_name = models.CharField(_("Last Name"), max_length=250)
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    date_joined = models.DateTimeField(_("Date Joined"),  auto_now_add=True)
    date_updated = models.DateTimeField(_(""), auto_now=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_verified = models.BooleanField(_("Is Verified"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self) -> str:
        return str(self.email)
    
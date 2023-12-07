from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model User.
    Stores all information about a user.
    """
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    firebase_uid = models.CharField(max_length=100, null=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Returns the full name of the user.
        :return: Full name of the user
        """
        return f'{self.firstname} {self.lastname} ({self.email})'

    def get_groups(self):
        """
        Returns all groups of the user.
        :return: QuerySet of groups
        """
        return self.groups.all()

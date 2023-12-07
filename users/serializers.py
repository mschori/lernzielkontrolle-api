from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class GroupSerializer(serializers.ModelSerializer):
    """
    Model-Serializer for Groups.
    """

    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    """
    Model-Serializer for Users.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'date_joined', 'last_login')

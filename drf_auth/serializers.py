from rest_framework import serializers

from users.models import User
from users.serializers import GroupSerializer


class TokenSerializer(serializers.Serializer):
    """
    Serializer for Tokens.
    """

    access = serializers.CharField()
    refresh = serializers.CharField()


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for User-Login.
    """
    tokens = TokenSerializer()
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'tokens', 'groups')

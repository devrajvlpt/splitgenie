from rest_framework import serializers
from .contact import UserSerializer
from coresetup.models.friend import Friend

class FriendsSerializer(serializers.ModelSerializer):
    """[summary]

    Args:
        serializers ([type]): [description]
    """
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        """[summary]
        """
        model = Friend
        fields = ['id', 'current_user', 'users']
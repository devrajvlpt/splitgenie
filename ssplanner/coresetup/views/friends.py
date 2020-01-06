# -*- coding: utf-8 -*-
#https://briancaffey.github.io/2017/07/19/different-ways-to-build-friend-models-in-django.html

from __future__ import unicode_literals

from coresetup.models.models import Friend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (    
    IsAuthenticated,
    AllowAny
)
from coresetup.serializers.serialiser import (
    FriendsSerializer
)


class FriendView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        friends = Friend.objects.filter(pk=request.user.id)
        friendsserializer = FriendsSerializer(friends, many=True)
        return Response(friendsserializer.data, status.HTTP_200_OK)

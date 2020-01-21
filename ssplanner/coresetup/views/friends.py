# -*- coding: utf-8 -*-
#https://briancaffey.github.io/2017/07/19/different-ways-to-build-friend-models-in-django.html

from __future__ import unicode_literals

from coresetup.models.models import (
    Friend,
    Contact
)
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

    def post(self, request):
        current_user = request.user.id
        user = request.data['user']
        # for user in users:
        current_contact = Contact.objects.filter(pk=current_user).first()
        create_friend = Friend.make_friend(
            current_user=current_contact,
            new_friend=user
        )
        if create_friend:
            friends = Friend.objects.filter(users=user)
            friendsserializer = FriendsSerializer(friends)
            return Response(friendsserializer.data, status.HTTP_201_CREATED)
        # TODO implement else part if not created


class FriendDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        friends = Friend.objects.filter(pk=pk)
        friendsserializer = FriendsSerializer(friends, many=True)
        return Response(friendsserializer.data, status.HTTP_200_OK)  
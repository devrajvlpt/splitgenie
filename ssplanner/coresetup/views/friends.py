# -*- coding: utf-8 -*-
#https://briancaffey.github.io/2017/07/19/different-ways-to-build-friend-models-in-django.html

from __future__ import unicode_literals

from coresetup.models.contact import Contact
from coresetup.models.friend import Friend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (    
    IsAuthenticated,
    AllowAny
)
from coresetup.serializers.friend import (
    FriendsSerializer
)


class FriendView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(request.user.id)
        friends = Friend.objects.filter(current_user=request.user.id)
        friendsserializer = FriendsSerializer(friends, many=True)
        return Response(friendsserializer.data, status.HTTP_200_OK)  

    def post(self, request):
        # TODO create user and add as friend(Split Directly)
        list_users = request.data
        print(list_users['user_list'])
        current_user = request.user.id
        current_contact = Contact.objects.filter(pk=current_user).first()
        for user in list_users['user_list']:
            contact, created = Contact.objects.get_or_create(
                user_name=user['user_name']
            )            
            if not created:
                contact.is_active = False
                contact.save()                
                create_friend = Friend.make_friend(
                    current_user=current_contact,
                    new_friend=contact
                )
            else:
                create_friend = Friend.make_friend(
                    current_user=current_contact,
                    new_friend=contact
                )
            
        friends = Friend.objects.filter(users=current_user)
        friendsserializer = FriendsSerializer(friends)
        return Response(friendsserializer.data, status.HTTP_201_CREATED)
        


class FriendDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        friends = Friend.objects.filter(current_user=request.user.id)
        friendsserializer = FriendsSerializer(friends, many=True)
        return Response(friendsserializer.data, status.HTTP_200_OK)  
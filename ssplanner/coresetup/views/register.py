# -*- coding: utf-8 -*-
# https://github.com/RealmTeam/django-rest-framework-social-oauth2
from __future__ import unicode_literals

from coresetup.models.models import Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from coresetup.serializers.serialiser import (
    ContactSerializer,
    UserSerializer
    )


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        contactserializer = ContactSerializer(data=request.data)
        if contactserializer.is_valid():
            contactserializer.save()
            return Response(
                contactserializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            contactserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RegisterDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        contacts = Contact.objects.all()
        userserializer = UserSerializer(contacts, many=True)
        return Response(userserializer.data)

# -*- coding: utf-8 -*-
# https://github.com/RealmTeam/django-rest-framework-social-oauth2
from __future__ import unicode_literals

from coresetup.models.contact import Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from coresetup.serializers.contact import (
    ContactSerializer,
    UserSerializer
    )


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        contact_exists = Contact.objects.filter(
            user_name=request.data['user_name']
        ).first()
        if contact_exists:
            contactserializer = ContactSerializer(contact_exists, data=request.data)
            if contactserializer.is_valid():
                contactserializer.save()
                return Response(
                    contactserializer.data,
                    status=status.HTTP_201_CREATED
                )
        else:
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

    def get(self, request):
        contacts = Contact.objects.all()
        userserializer = UserSerializer(contacts, many=True)
        return Response(userserializer.data)


class RegisterDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        contact = Contact.objects.filter(
            id=pk
        ).first()
        userserializer = UserSerializer(contact)
        return Response(userserializer.data)

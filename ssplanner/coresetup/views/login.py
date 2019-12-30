# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.response import Response
from oauth2_provider.models import Application
from rest_framework.permissions import AllowAny
from coresetup.serializers.serialiser import (
    ApplicationListSerializer,
    SocialAuthSerializer
)


class LoginView(View):

    def post(self, request):
        pass

    def get(self, request):
        pass


class LogoutView(View):

    def post(self, request):
        pass


class ApplicationListView(APIView):
    
    def get(self, request):
        applications = Application.objects.all()
        appserializer = ApplicationListSerializer(applications, many=True)
        return Response(appserializer.data)


class SocialAuthAssociationView(APIView):

    def post(self, request):
        socialserializer = SocialAuthSerializer(data=request.data)
        if socialserializer.is_valid():
            socialserializer.save()
            return Response(
                socialserializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            socialserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SocialSignUP(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
        ):
    #https://hashedin.com/blog/a-guide-to-using-social-login-with-django/
    
    permission_classes = (AllowAny,)

    def create(self, reques, *args, **kwargs):
        redirect = request.path        
        try:
            provider = request.DATA['provider']
            #figure out what is access token
            access_token = request.DATA['access_token'] 
        except KeyError:
            return Response({
                'success':False,
                'detail': "'provider' and 'access token' are required parameters"
            })
        backend = get_backend(provider, request, redirect)
        if access_token:
            print (provider)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import serializers
from django.contrib.auth import authenticate
# Create your views here.
# from coresetup.models.models import (
#     Contact,
#     Topic,
#     SubTopic,
#     SplitAmountLedger,
#     Friend,
#     SplitOrder
# )
from oauth2_provider.models import Application
from social_django.models import UserSocialAuth


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class SocialAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSocialAuth
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=240)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        user_name = data.get('user_name', None)
        # email = data.get('email', None)
        password = data.get('password', None)
        mobile_number = data.get('mobile_number', None)

        # Raise an exception if an
        # email is not provided.
        # if email is None:
        #     raise serializers.ValidationError(
        #         'An email address is required to log in.'
        #     )
        if user_name is None:
            raise serializers.ValidationError(
                'A Mobile Number is required to log in'
            )
        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(
            # mobile_number=mobile_number,
            user_name=user_name,
            password=password
        )

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this mobile_number and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'user_name': user.user_name,
            'first_name': user.first_name,
            'token': user.token
        }



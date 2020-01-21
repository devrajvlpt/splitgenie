# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth import authenticate
# Create your views here.
from coresetup.models.models import (
    Contact,
    Topic,    
    SplitAmountLedger,
    Friend
)
from oauth2_provider.models import Application
from social_django.models import UserSocialAuth

class ContactSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    """ Description	"""

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        contact = Contact(
            mobile_number=validated_data['mobile_number'],
            last_login=datetime.now(),
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        contact.set_password(validated_data['password'])
        contact.save()
        return contact


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = [
            'id', 'mobile_number', 'last_login',
            'email', 'first_name',
            'last_name', 'registered_time',
            ]


class FriendsSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Friend
        fields = ['id', 'current_user', 'users']


class TopicSerializer(serializers.ModelSerializer):
    # created_by = UserSerializer()
    # updated_by = UserSerializer()
    """Summary
    """
    class Meta:

        """Summary
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """
        model = Topic
        fields = '__all__'

    def create(self, validated_data):
        topic = Topic(
            topic_name=validated_data['topic_name'],
            total_amount=validated_data['total_amount'],
            created_by=validated_data['created_by'],
            updated_by=validated_data['updated_by']
        )      
        topic.save()
        return topic


class TopicDetailSerializer(serializers.ModelSerializer):
    """Summary
    """
    class Meta:

        """Summary
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """
        model = Topic
        fields = '__all__'


class SplitLedgerSerializer(serializers.ModelSerializer):

    """Summary
    """
    # topic_id = TopicSerializer(read_only=True, many=True)
    # splitted_user = UserSerializer(read_only=True, many=True)
    # created_by = UserSerializer(read_only=True)
    # updated_by = UserSerializer(read_only=True)

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = SplitAmountLedger
    	fields = '__all__'


class SplitLedgerDetailSerializer(serializers.ModelSerializer):
    topic_id = TopicSerializer(read_only=True)
    splitted_user = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = SplitAmountLedger
    	fields = '__all__'



class ApplicationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Application
        fields = '__all__'


class SocialAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSocialAuth
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.IntegerField()
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        print(data, 'serializer valid method')
        mobile_number = data.get('mobile_number', None)
        print(mobile_number)
        # email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        # if email is None:
        #     raise serializers.ValidationError(
        #         'An email address is required to log in.'
        #     )
        if mobile_number is None:
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
        user = authenticate(mobile_number=mobile_number, password=password)
        print(user, 'RAIN BUCKET')

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
        print(user.first_name)
        return {
            'mobile_number': user.mobile_number,
            'first_name': user.first_name,
            'token': user.token
        }

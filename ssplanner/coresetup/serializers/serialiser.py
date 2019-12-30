# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers
from datetime import datetime

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
        fields = ['current_user', 'users']


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


class SplitLedgerSerializer(serializers.ModelSerializer):

    """Summary
    """
    topic_id = TopicSerializer(read_only=True)
    splitted_user = UserSerializer(read_only=True)
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


class ApplicationListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Application
        fields = '__all__'


class SocialAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSocialAuth
        fields = '__all__'
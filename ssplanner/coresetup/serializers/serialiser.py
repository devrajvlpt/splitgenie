# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers
from datetime import datetime

# Create your views here.
from coresetup.models.models import (
    Contact,
    Topic,
    SplitAmountLedger
)


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
            'mobile_number', 'last_login',
            'email', 'first_name',
            'last_name', 'registered_time',
            ]
    

class TopicSerializer(serializers.ModelSerializer):

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
    topic =  TopicSerializer()

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = SplitAmountLedger
    	fields = '__all__'

    def create(self, validated_data):
        """Summary
        
        Args:
            validated_data (TYPE): Description
        """
        topic_data = validated_data.pop('topic')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers

# Create your views here.
from .models import (
	Topic, 
	SplitAmountLedger
)

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
        


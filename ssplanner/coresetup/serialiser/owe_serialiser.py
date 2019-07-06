# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import serializers
from coresetup.models.owe_model import OweModel 

class OweSerializer(serializers.ModelSerializer):

    """Summary
    """
    topic =  TopicSerializer()

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = OweModel
    	fields = '__all__'


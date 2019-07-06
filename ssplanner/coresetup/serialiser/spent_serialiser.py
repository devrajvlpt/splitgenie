# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import serializers
from coresetup.models.spent_model import SpentModel

class SpentModelSerializer(serializers.ModelSerializer):

    """Summary
    """
    class Meta:

    	"""Summary
        
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """

    	model = SpentModel
    	fields = '__all__'

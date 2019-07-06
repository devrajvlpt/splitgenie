# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import serializers
from coresetup.models.contact_model import Contact

class ContactModelSerializer(serializers.ModelSerializer):

    """Summary
    """
    class Meta:

    	"""Summary
        
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """

    	model = Contact
    	fields = '__all__'

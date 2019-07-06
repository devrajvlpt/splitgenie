
# -*- coding: utf-8 -*-
# python manage.py make migrations your_app_label
# python manage.py migrate --fake-initial your_app_label

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import date, datetime
from django.conf import settings

class SpentModel(models.Model):

    """SpentModel based on amount Spent by the person
    
    Attributes:
        created_at (TYPE): Description
        created_by (TYPE): Description
        split_number (TYPE): Description
        total_amount (TYPE): Description
        updated_at (TYPE): Description
        updated_by (TYPE): Description
    """
    
    spent_amount = models.IntegerField()
    spent_on = models.CharField(max_length=80, blank=True)
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'topic_created', 
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL, 
                            related_name= 'topic_updated',
                            on_delete=models.CASCADE
                        )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
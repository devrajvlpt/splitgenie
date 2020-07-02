from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """    
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

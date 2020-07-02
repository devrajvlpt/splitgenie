from django.db import models
from .auditlog import AuditLog
from django.conf import settings

class Topic(AuditLog):

    """Topic based on share is created

    Attributes:
        created_at (TYPE): Description
        created_by (TYPE): Description
        split_number (TYPE): Description
        total_amount (TYPE): Description
        updated_at (TYPE): Description
        updated_by (TYPE): Description
    """
    topic_name = models.CharField(
        max_length=240,
        default="splitztopic"
    )
    topic_description = models.CharField(
        max_length=240,
        default="Sharing with Friends and Families"
    )    
    total_amount = models.IntegerField()
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name="topic_created",
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name="topic_updated",                        
                            on_delete=models.CASCADE
                        )
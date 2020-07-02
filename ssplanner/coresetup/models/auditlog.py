from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    created_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='audit_created',
                            on_delete=models.CASCADE
                        )
    updated_by = models.ForeignKey(
                            settings.AUTH_USER_MODEL,
                            related_name='audit_updated',
                            on_delete=models.CASCADE
                        )
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

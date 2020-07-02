from django.db import models
from .auditlog import AuditLog
from django.conf import settings
from .sub_topic import SubTopic


class SplitAmountLedger(AuditLog):

    """List of splitted amount to each user under same topic
    Attributes:
        created_at (TYPE): Description
        created_by (TYPE): Description
        splitted_amount (TYPE): Description
        splitted_user (TYPE): Description
        updated_at (TYPE): Description
        updated_by (TYPE): Description
    """    
    splitted_user = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                related_name='sa_ledger_user',
                                on_delete=models.CASCADE
                            )
    splitted_amount = models.IntegerField()
    splitted_descriptions = models.CharField(max_length=80, blank=True, default='')
    sub_topic_id = models.ForeignKey(
            SubTopic,
            related_name='sub_topic_ledger',
            on_delete=models.CASCADE,
            blank=True
    )
    
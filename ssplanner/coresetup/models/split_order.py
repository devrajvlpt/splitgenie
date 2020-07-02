from django.db import models
from .auditlog import AuditLog
from datetime import datetime


class SplitOrder(AuditLog):
    """[summary]

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    order_id = models.CharField(max_length=80, blank=True, default='', unique=True)
    entity = models.CharField(max_length=80, blank=True, default='')    
    amount = models.IntegerField(blank=True, default=0)
    amount_paid = models.IntegerField(blank=True, default=0)
    amount_due = models.IntegerField(blank=True, default=0)
    currency = models.CharField(max_length=80, blank=True, default='')
    attempts = models.IntegerField(blank=False, default=0)
    status = models.CharField(max_length=80, blank=True, default="error")
    receipt = models.CharField(max_length=80, blank=True, default='')
    offer_id = models.CharField(max_length=240, blank=True, default='')
    notes = models.CharField(max_length=254, blank=True, default='')
    payment_capture = models.BooleanField(default=True)
    order_created = models.DateTimeField(default=datetime.now())
    

    def __str__(self):
        return str("{} - {}".format(self.amount, self.currency))
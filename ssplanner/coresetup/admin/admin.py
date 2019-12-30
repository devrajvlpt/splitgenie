# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from coresetup.models.models import Contact, Topic, SplitAmountLedger

admin.site.register(Contact)
admin.site.register(Topic)
admin.site.register(SplitAmountLedger)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from coresetup.models.models import (
    SplitAmountLedger,
    Topic,
    Contact
)
from coresetup.serializers.serialiser import (
    SplitLedgerSerializer
)


class SplitzAggregator(object):

    def set_splitted_amount(self, validated_data):
        splitz_amount = {}
        split_amount = (
                validated_data['total_amount'] /
                len(validated_data['users'])
            )
        counter = 0
        for user in validated_data['users']:
            splitz_amount['splitted_user'] = user
            splitz_amount['splitted_amount'] = split_amount
            splitz_amount['topic_id'] = validated_data['topic_id']
            splitz_amount['created_by'] = validated_data['created_by']
            splitz_amount['updated_by'] = validated_data['updated_by']
            splitz = SplitLedgerSerializer(data=splitz_amount)
            if splitz.is_valid():
                splitz.save()
            counter += 1
            if counter == len(validated_data['users']):
                break
        return True

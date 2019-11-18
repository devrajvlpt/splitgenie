# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from coresetup.models.models import (
    SplitAmountLedger,
    Topic
)
import copy


class SplitzAggregator(object):

    def get_splitted_amount(self, validated_data):
        
        user_list = []
        len_of_splitz = SplitAmountLedger.objects.filter(
            topic_id=validated_data['topic_id']
        ).count()

        total_amount = Topic.objects.filter(
                id=validated_data['topic_id']
                ).values('total_amount')

        if len_of_splitz == 0:
            # initial insert both
            user_list.append(validated_data)
            initial_data = copy.deepcopy(validated_data)
            initial_data['splitted_user'] = validated_data['created_by']
            user_list.append(initial_data)

            validated_data['splitted_amount'] = int(
                total_amount[0].get(
                    'total_amount', 0
                    )/user_list
                )
            return user_list
        else:
            # one insert others update
            validated_data['splitted_amount'] = total_amount[0].get(
                'total_amount', 0) / (len_of_splitz + 1)
            user_list.append(validated_data)

            update_amount = SplitAmountLedger.objects.filter(
                topic_id=validated_data['topic_id']
            )
            for update in update_amount:
                update['splitted_amount'] = total_amount[0].get(
                            'total_amount', 0) / (len_of_splitz + 1)
                user_list.append(update)
            return user_list

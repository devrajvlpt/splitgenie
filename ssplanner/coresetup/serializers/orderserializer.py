from __future__ import unicode_literals

from rest_framework import serializers

from coresetup.models.split_order import (
    SplitOrder
)


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    order_created = serializers.SerializerMethodField()

    class Meta:
        model = SplitOrder
        fields = '__all__'

    def get_order_id(self, obj):
        return obj.id

    def get_order_created(self, obj):
        return obj.order_created

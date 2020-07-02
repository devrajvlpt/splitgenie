from rest_framework import  serializers
from coresetup.models.split_order import SplitOrder
from datetime import datetime

class SplitOrderSerializer(serializers.ModelSerializer):
    # id = serializers.Field(source="order_id")

    class Meta:
        model = SplitOrder
        fields = (
            "order_id",
            "entity",
            "amount",
            "amount_paid",
            "amount_due",
            "currency",
            "attempts",
            "status",
            "receipt",
            "offer_id",
            "notes",
            "payment_capture",
            "order_created",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        )
    
    def create(self, validated_data):
        splitorder = SplitOrder(
            order_id = validated_data['order_id'],
            entity = validated_data['entity'],
            amount = validated_data['amount'],
            amount_paid = validated_data['amount_paid'],
            amount_due = validated_data['amount_due'],
            currency = validated_data['currency'],
            attempts = validated_data['attempts'],
            status = validated_data['status'],
            receipt = validated_data['receipt'],
            offer_id = validated_data['offer_id'],
            notes = validated_data['notes'],
            payment_capture = validated_data['payment_capture'],
            order_created = validated_data['order_created'] or datetime.now(),
            created_by = validated_data['created_by'],
            updated_by = validated_data['updated_by'],
            # created_at = validated_data['created_at'],
            # updated_at  = validated_data['created_at']
        )
        splitorder.save()
        return splitorder
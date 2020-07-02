from rest_framework import serializers
from coresetup.models.split_ledger import SplitAmountLedger
from .sub_topic import SubTopicSerializer
from .contact import UserSerializer


class SplitLedgerSerializer(serializers.ModelSerializer):

    """Summary
    """
    # topic_id = TopicSerializer(read_only=True, many=True)
    # splitted_user = UserSerializer(read_only=True, many=True)
    # created_by = UserSerializer(read_only=True)
    # updated_by = UserSerializer(read_only=True)

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = SplitAmountLedger
    	fields = '__all__'

    def update(self, instance, validated_data):
        instance.splitted_amount = validated_data.get('splitted_amount', instance.splitted_amount)
        instance.splitted_user = validated_data.get('splitted_user', instance.splitted_user)
        instance.topic_id = validated_data.get('topic_id', instance.topic_id)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)        
        instance.save()
        return instance


class SplitLedgerDetailSerializer(serializers.ModelSerializer):
    sub_topic_id = SubTopicSerializer(read_only=True)
    splitted_user = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:

    	"""Summary
    	
    	Attributes:
    	    fields (str): Description
    	    model (TYPE): Description
    	"""

    	model = SplitAmountLedger
    	fields = '__all__'

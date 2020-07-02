from rest_framework import serializers
from coresetup.models.topic import Topic


class TopicSerializer(serializers.ModelSerializer):    
    """Summary
    """
    class Meta:

        """Summary
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """
        model = Topic
        fields = '__all__'

    def create(self, validated_data):
        topic = Topic(
            topic_name=validated_data['topic_name'],
            topic_description=validated_data['topic_description'],
            total_amount=validated_data['total_amount'],
            created_by=validated_data['created_by'],
            updated_by=validated_data['updated_by']
        )      
        topic.save()
        return topic
        

class TopicDetailSerializer(serializers.ModelSerializer):
    """Summary
    """
    class Meta:

        """Summary
        Attributes:
            fields (str): Description
            model (TYPE): Description
        """
        model = Topic
        fields = '__all__'

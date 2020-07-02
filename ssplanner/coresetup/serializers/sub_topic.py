from rest_framework import serializers
from coresetup.models.sub_topic import SubTopic

class SubTopicSerializer(serializers.ModelSerializer):
    """[summary]

    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """
    class Meta:
        """[summary]
        """
        model = SubTopic
        fields = (
            "id",
            "sub_topicname",
            "sub_topicamount",
            "sub_topicdescription",
            "topic_id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        """[summary]

        Args:
            validated_data ([type]): [description]

        Returns:
            [type]: [description]
        """
        sub_topic = SubTopic(
            sub_topicname=validated_data['sub_topicname'],
            sub_topicdescription=validated_data['sub_topicdescription'],
            sub_topicamount=validated_data['sub_topicamount'],
            topic_id=validated_data['topic_id'],
            created_by=validated_data['created_by'],
            updated_by=validated_data['updated_by']
        )      
        sub_topic.save()
        return sub_topic

class SubTopicDetailSerializer(serializers.ModelSerializer):
    """[summary]

    Args:
        serializers ([type]): [description]
    """


    class Meta:
        """[summary]
        """
        model = SubTopic
        fields = "__all__"


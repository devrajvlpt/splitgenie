from __future__ import unicode_literals

from coresetup.models.topic import (
    Topic
)
from django.shortcuts import get_object_or_404
from rest_framework.views import (
    APIView,
)
from rest_framework.generics import(
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from coresetup.serializers.sub_topic import (
    SubTopicSerializer,
    SubTopicDetailSerializer
    
)
from coresetup.models.sub_topic import SubTopic
from coresetup.models.split_ledger import SplitAmountLedger


class SubSectionView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        sub_topic = SubTopicSerializer(data=request.data)
        if sub_topic.is_valid(raise_exception=True):
            sub_topic.save()
            return Response(
                sub_topic.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            sub_topic.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):

        topic_created = SubTopic.objects.filter(
            created_by=request.user.id
            ).all()
        list_sub_topics = [topic for topic in topic_created]        
        splitz_user = SplitAmountLedger.objects.filter(
            splitted_user=request.user.id
        ).exclude(created_by=request.user.id).all()
        for splitz in splitz_user:
            sub_topic_participated = SubTopic.objects.filter(
                id=splitz.sub_topic_id.id
            ).first()            
            if list_sub_topics:
                list_sub_topics.append(sub_topic_participated)
            else:
                list_sub_topics.append(sub_topic_participated)        
        topicserializer = SubTopicDetailSerializer(list_sub_topics, many=True)
        return Response(
            topicserializer.data,
            status=status.HTTP_200_OK
        )
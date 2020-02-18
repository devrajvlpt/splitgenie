# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from coresetup.models.models import (
    Topic,    
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
from coresetup.serializers.serialiser import (
    TopicSerializer,    
    TopicDetailSerializer,
    SplitLedgerDetailSerializer,
    SplitLedgerSerializer
)
from coresetup.models import SplitAmountLedger
from coresetup.splitz.splitz_aggregator import (
    SplitzAggregator
)


class TopicView(APIView):
    permission_classes = (IsAuthenticated, )
    splitz_aggregator = SplitzAggregator()

    def post(self, request):             
        topic = TopicSerializer(data=request.data)
        if topic.is_valid(raise_exception=True):
            topic.save()
            return Response(
                topic.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            topic.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):

        topic_created = Topic.objects.filter(
            created_by=request.user.id
            ).all()
        list_topics = [topic for topic in topic_created]        
        splitz_user = SplitAmountLedger.objects.filter(
            splitted_user=request.user.id
        ).exclude(created_by=request.user.id).all()
        for splitz in splitz_user:
            topic_participated = Topic.objects.filter(
                id=splitz.topic_id.id
            ).first()            
            if list_topics:
                list_topics.append(topic_participated)
            else:
                list_topics.append(topic_participated)        
        topicserializer = TopicDetailSerializer(list_topics, many=True)
        return Response(
            topicserializer.data,
            status=status.HTTP_200_OK
        )


class TopicDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)    
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    
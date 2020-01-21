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
    TopicDetailSerializer
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
        splitzs = SplitAmountLedger.objects.filter(
            splitted_user=request.user.id
        ).all()
        topics = []
        for splitz in splitzs:
            topic = Topic.objects.filter(
                id=splitz.topic_id.id
                ).first()
            topicserializer = TopicDetailSerializer(topic)
            topics.append(topicserializer.data)
        return Response(
            topics,
            status=status.HTTP_200_OK
        )


class TopicDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)    
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    
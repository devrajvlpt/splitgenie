# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from coresetup.models.models import Topic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from coresetup.serializers.serialiser import (
    TopicSerializer
)


class TopicView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):

        topic = TopicSerializer(data=request.data)
        if topic.is_valid():
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
        topics = Topic.objects.all()
        topicserializer = TopicSerializer(topics, many=True)
        return Response(
            topicserializer.data,
            status=status.HTTP_200_OK
            )

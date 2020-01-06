# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from coresetup.models.models import (
    Topic,
    TopicMembers
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_get_user_id_from_payload_handler
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from coresetup.serializers.serialiser import (
    TopicSerializer,
    TopicMemberSerializer,
    TopicDetailSerializer
)
from coresetup.splitz.splitz_aggregator import (
    SplitzAggregator
)


class TopicView(APIView):
    permission_classes = (IsAuthenticated, )
    splitz_aggregator = SplitzAggregator()

    def post(self, request):     
        print(request.data)
        topic = TopicSerializer(data=request.data)
        if topic.is_valid(raise_exception=True):
            topic.save()
            topic_member = {'current_user': request.user.id}
            for user in request.data['members_list']:
                topic_member['user'] = user
                member_serialiser = TopicMemberSerializer(data=topic_member)
                if member_serialiser.is_valid(raise_exception=True):
                    member_serialiser.save()
            request.data['topic_id'] = topic.data['id']
            aggregated_data = TopicView.splitz_aggregator.set_splitted_amount(
                request.data
            )
            if aggregated_data:
                return Response(
                    topic.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            topic.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):        
        topics = Topic.objects.filter(created_by=request.user.id)
        topicserializer = TopicDetailSerializer(topics, many=True)
        return Response(
            topicserializer.data,
            status=status.HTTP_200_OK
            )

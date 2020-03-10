# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from coresetup.models.models import SplitAmountLedger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from coresetup.models import (
    Topic,
    Contact
)
from coresetup.serializers.serialiser import (
    SplitLedgerSerializer,
    SplitLedgerDetailSerializer
)
from coresetup.splitz.splitz_aggregator import (
    SplitzAggregator
)


class SplitzView(APIView):
    permission_classes = (IsAuthenticated, )
    splitz_aggregator = SplitzAggregator()

    def post(self, request):
        splitz_amount = {}
        print(request.data['topic_id'])
        topic = Topic.objects.filter(id=request.data['topic_id']).first()
        split_exists = SplitAmountLedger.objects.filter(
            topic_id=request.data['topic_id']
        ).all()
        print(len(request.data['members_list']) + len(split_exists))
        split_amount = round(
                topic.total_amount /
                len(request.data['members_list']) + len(split_exists)
            )
        counter = 0
        if split_exists:
            for user in request.data['members_list']:
                contact, created = Contact.objects.get_or_create(
                    user_name=user
                )     
                if not created:
                    contact.is_active = False
                    contact.save()
                    splitz_amount['splitted_user'] = int(contact.id)
                else:
                    splitz_amount['splitted_user'] = int(contact.id)
                splitz_amount['splitted_amount'] = int(split_amount)
                splitz_amount['topic_id'] = request.data['topic_id']
                splitz_amount['created_by'] = request.user.id
                splitz_amount['updated_by'] = request.user.id
                splitz = SplitLedgerSerializer(data=splitz_amount)
                if splitz.is_valid(raise_exception=True):
                    splitz.save()
                counter += 1
                if counter == len(request.data['members_list']):
                    break
            for exists_user in split_exists:
                splitz_amount['splitted_user'] = int(exists_user.splitted_user.id)
                splitz_amount['splitted_amount'] = int(exists_user.splitted_amount)
                splitz_amount['topic_id'] = exists_user.topic_id.id
                splitz_amount['created_by'] = request.user.id
                splitz_amount['updated_by'] = request.user.id
                splitz = SplitLedgerSerializer(data=splitz_amount)
                if splitz.is_valid(raise_exception=True):
                    splitz.save()
        else:
            for user in request.data['members_list']:
                contact, created = Contact.objects.get_or_create(
                    user_name=user
                )                
                if not created:
                    contact.is_active = False
                    contact.save()
                    splitz_amount['splitted_user'] = int(contact.id)
                else:
                    splitz_amount['splitted_user'] = int(contact.id)
                splitz_amount['splitted_amount'] = int(split_amount)
                splitz_amount['topic_id'] = request.data['topic_id']
                splitz_amount['created_by'] = request.user.id
                splitz_amount['updated_by'] = request.user.id
                splitz = SplitLedgerSerializer(data=splitz_amount)
                if splitz.is_valid(raise_exception=True):
                    splitz.save()
                counter += 1
                if counter == len(request.data['members_list']):
                    break

        return Response(
            'Users added successfully',
            status=status.HTTP_201_CREATED
            )

    def get(self, request):
        topics = SplitAmountLedger.objects.all()
        splitzserializer = SplitLedgerSerializer(topics, many=True)
        return Response(
            splitzserializer.data,
            status=status.HTTP_200_OK
            )


class SplitzDetailView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        splitz_details = SplitAmountLedger.objects.filter(
            topic_id=pk,
            splitted_user=request.user.id
            )
        splitzserializer = SplitLedgerDetailSerializer(
            splitz_details,
            many=True
        )
        return Response(
            splitzserializer.data,
            status=status.HTTP_200_OK
            )
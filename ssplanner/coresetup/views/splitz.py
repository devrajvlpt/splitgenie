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
from coresetup.serializers.serialiser import (
    SplitLedgerSerializer,
    SplitLedgerDetailSerializer
)
from coresetup.splitz.splitz_aggregator import (
    SplitzAggregator
)


class SplitzView(APIView):
    permission_classes = (AllowAny, )
    splitz_aggregator = SplitzAggregator()

    def post(self, request):

        aggregated_data = SplitzView.splitz_aggregator.get_splitted_amount(
            request.data
        )
        len_of_splitz = SplitAmountLedger.objects.filter(
            topic_id=request.data['topic_id']
        ).count()
        if len_of_splitz == 0:
            for data in aggregated_data:
                splitz = SplitLedgerSerializer(data=data)
                if splitz.is_valid():
                    splitz.save()
                    return Response(
                        splitz.data,
                        status=status.HTTP_201_CREATED
                    )
        else:
            # for data in aggregated_data:

            return Response(
                splitz.errors,
                status=status.HTTP_400_BAD_REQUEST
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
            ).exclude(splitted_user=request.user.id)
        splitzserializer = SplitLedgerDetailSerializer(splitz_details, many=True)
        return Response(
            splitzserializer.data,
            status=status.HTTP_200_OK
            )
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
from coresetup.models.models import (
    Topic,
    SubTopic,
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
        sub_topic = SubTopic.objects.filter(id=request.data['sub_topic_id']).first()
        
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
            splitz_amount['splitted_amount'] = request.data['amount']
            splitz_amount['splitted_descriptions'] = request.data['splitted_descriptions']
            splitz_amount['sub_topic_id'] = sub_topic.id
            splitz_amount['created_by'] = request.user.id
            splitz_amount['updated_by'] = request.user.id
            splitz = SplitLedgerSerializer(data=splitz_amount)
            if splitz.is_valid(raise_exception=True):
                splitz.save()
            # update subtopic amount everytime a new user added
            sub_topic.sub_topicamount += int(request.data['amount'])
        
        # Finall updated on the total amount
        sub_topic.save()

        # TODO Need to work on failure cases. Only success cases handled

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
    model = SplitAmountLedger
    admin = False

    def admin_user(func):
        def wrapper(*args, **kwargs):
            sub_topic = SubTopic.objects.filter(
                topic_id=kwargs['pk']
            ).first()
            if sub_topic:
                admin = args[0].model.objects.filter(
                    created_by=args[1].user.id,
                    sub_topic_id=sub_topic.id
                )
                if admin:
                    args[0].admin = True
                    return func(*args, **kwargs)
                return func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    @admin_user
    def get(self, request, pk, format=None):
        sub_topics = SubTopic.objects.filter(
            topic_id=pk
        ).all()
        
        if len(sub_topics) > 0:
            splitz_details = []
            for sub in sub_topics:
                splitz_sub = SplitAmountLedger.objects.filter(
                    sub_topic_id=sub.id
                ).all()
                splitz_details.extend(splitz_sub)
            if splitz_details:                
                if self.admin:
                    splitz_details = [details for details in splitz_details if details.created_by_id==request.user.id]
                else:
                    splitz_details = [details for details in splitz_details if details.splitted_user_id==request.user.id]
                
                splitzserializer = SplitLedgerDetailSerializer(
                    splitz_details,
                    many=True
                )
                
                for data in splitzserializer.data:
                    data["admin"] = self.admin                
                return Response(
                    splitzserializer.data,
                    status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    [],
                    status=status.HTTP_200_OK
                    )
        else:
            return Response(
                [],
                status=status.HTTP_200_OK
                )


    
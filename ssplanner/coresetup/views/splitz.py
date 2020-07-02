# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from coresetup.models.split_ledger import SplitAmountLedger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
# from coresetup.models.topic import Topic
from coresetup.models.sub_topic import SubTopic
from coresetup.models.contact import Contact

from coresetup.serializers.split_ledger import (
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


class SplitzSubTopic(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Get the sub_topic_id and calulated the splitted amount across the users
        sub_topic_id = request.data['sub_topic_id']
        print(sub_topic_id)
        pre_splitz_amount = SplitAmountLedger.objects.filter(
                sub_topic_id=sub_topic_id
            ).all()
        if pre_splitz_amount:
            # finding the common sum amongst them
            pre_total_sum = 0
            common_sum = 0
            for sub in pre_splitz_amount:
                pre_total_sum += sub.splitted_amount
                common_sum = pre_total_sum / len(pre_splitz_amount)

            # Using common sum we can calulate owe and spent
            for owe_spent in pre_splitz_amount:
                if owe_spent.splitted_amount > common_sum:
                    owe_spent.owe = 0
                    owe_spent.spent = owe_spent.splitted_amount - common_sum
                elif owe_spent.splitted_amount < common_sum:
                    owe_spent.owe = common_sum - owe_spent.splitted_amount
                    owe_spent.spent = 0
                elif owe_spent.splitted_amount == common_sum:
                    owe_spent.owe = 0
                    owe_spent.spent = 0
            
            # calulate the actual splitz
            for final_sum  in pre_splitz_amount:
                list_of_owes_users = []
                list_of_gains_users = []
                for match in pre_splitz_amount:
                    if match.owe > 0:
                        if match.owe >= final_sum.spent:
                            list_of_owes_users.append(match.splitted_user_id)
                            final_sum.gains_me = list_of_owes_users
                            final_sum.spent = match.owe - final_sum.spent
                        elif match.owe < final_sum.spent:
                            list_of_owes_users.append(match.splitted_user_id)
                            final_sum.gains_me = list_of_owes_users
                            final_sum.spent = final_sum.spent - match.owe
            response = []
            for amount in pre_splitz_amount:
                splitz = SplitLedgerSerializer(data=amount) 
                if splitz.is_valid():
                    splitz.save()
                    response.append(splitz.data)
                else:
                    return Response(splitz.errors, status=status.HTTP_200_OK)
            if response:
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_412_PRECONDITION_FAILED)








from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (    
    AllowAny
)
from coresetup.models.split_order import SplitOrder
from coresetup.serializers.split_order import SplitOrderSerializer
import razorpay
from datetime import datetime

#Gloabl variable for razorpay client
CLIENT = razorpay.Client(
            auth=("rzp_test_XwIPUhyvVzTXkX", "ip1f8P4CBrSwMX00DINeHsuF")
        )
CLIENT.set_app_details(
    {
        "title":"Splitz",
        "version":"v.0.0.1"
    }
)

class OrderInterfaceView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        # { 
        #     'amount': 50000,
        #     'currency': 'INR',
        #     'receipt': 'order_rcptid_11',
        #     'notes': {'Shipping address': 'Bommanahalli, Bangalore'},
        #     'payment_capture': 1
        # }
        response = CLIENT.order.create(data=request.data)
        if response:
            response["order_id"] = response["id"]
            response['created_by'] = request.user.id or 4
            response['updated_by'] = request.user.id or 4
            response['notes'] = str(response['notes'])
            response['offer_id'] = ""
            if not response.get('payment_capture', ''):                
                response["payment_capture"] = False
            if not response.get('order_created', ''):
                response["order_created"] = datetime.now()                
            if response['id'] and response['created_at']:
                del response['id']
                del response['created_at']            
            splitorderserializer = SplitOrderSerializer(data=response)
            if splitorderserializer.is_valid(raise_exception=True):
                splitorderserializer.save()
                return Response(
                    splitorderserializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response("{}", status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        response = CLIENT.order.fetch_all()
        return Response(response, status.HTTP_200_OK)

# class PaymentInterfaceView(APIView):

#     permission_class = (AllowAny, )

#     def post(self, request):
        

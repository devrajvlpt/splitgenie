

from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (    
    AllowAny
)
import razorpay

#Gloabl variable for razorpay client
CLIENT = razorpay.Client(
            auth=("rzp_test_XwIPUhyvVzTXkX", "ip1f8P4CBrSwMX00DINeHsuF")
        )


class OrderInterfaceView(APIView):

    permission_classes = (AllowAny, )

    def post(self, request):
        DATA = { 
            'amount': 50000,
            'currency': 'INR',
            'receipt': 'order_rcptid_11',
            'notes': {'Shipping address': 'Bommanahalli, Bangalore'},
            'payment_capture': 1
        }
        response = CLIENT.order.create(data=DATA)
        return Response(response, status.HTTP_201_CREATED)

    def get(self, request):

        response = CLIENT.order.fetch_all()
        return Response(response, status.HTTP_200_OK)

# class PaymentInterfaceView(APIView):

#     permission_class = (AllowAny, )

#     def post(self, request):
        

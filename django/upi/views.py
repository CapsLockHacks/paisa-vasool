import json, re
from upi.models import Group, Contact, Subscription, Payment
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from upi.serializers import GroupSerializer, ContactSerializer,PaymentSerializer, SubscriptionSerializer

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class SubscriptionList(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # def perform_create(self, serializer):
    #     # create a payment entry with payment status as pending
    #     print("Hey I am called")

class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SyncSMS(APIView):
    """
    Sync SMS with mobile app.
    """

    def post(self, request, format=None):
        # serializer = SnippetSerializer()
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        list_of_sms = request.data

        for sms in list_of_sms:
            try:
                result = re.search(r'(\d+\.\d+)', sms)
                money = result.group()
            except:
                print("unable to find money")
                return Response(status=400)
            try:
                sub = Subscription.objects.get(amount=money)
            except Subscription.DoesNotExist:
                print("unable to find sub")
                return Response(status=400, data="amount not found")
            except Exception as e:
                print(e)
                return Response(status=500, data="something went wrong while fetching sub")
            try:
                Payment.objects.create(
                    status='complete',
                    contact = sub.contact,
                    group = sub.group,
                    amount = money
                )
            except:
                print("unable to create payment")
                return Response(status=400) 
        

        return Response(status=200)
import json, re
from upi.models import Group, Contact, Subscription, Payment
from django.http import Http404
from decimal import Decimal
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
                payment = Payment.objects.create(
                    status='complete',
                    contact = sub.contact,
                    group = sub.group,
                    amount = money
                )
            except Exception as e:
                print(f"unable to create payment {e}")
                return Response(status=400) 

            sub.last_payment_id = payment

            try:
                sub.save()
            except Exception as e:
                print(e)
                return Response(status=400, data="error while saving sub")

        return Response(status=200)


class Splits(APIView):
    """
    Creates multiple subscription entries for each group/contact 
    amount split.
    {
        "splits": [
            {
                "amount":"xyz",
                "contact": "abc",
            },
            ...
        ],
        "subscription": "netflix",
        "frequency": 8,
        "description": "hey this group is for netflix
    }

    """
    def get(self, request, format=None):
        subscriptions = Subscription.objects.all()
        data = []
        for sub in subscriptions:
            paid, unpaid = sub.get_settlement_status()
            if unpaid:
                settlement_status = True
            subscription_id = sub.id
            amount = sub.amount
            name = sub.name
            created_date = sub.created_date
            frequency = sub.frequency
            contacts = []
            groups = sub.get_all_groups()
            for i in groups:
                contacts.append({"name":i.contact.name,"amount":i.contact.amount,"settled": is_contact_settled(i.contact)})
            data.append({
                "settlement_status":settlement_status,
                "amount":amount,
                "name":name,
                "created_date":created_date,
                "frequency":frequency,
                "contacts":contacts
            })
        return Reponse(status=200, data=data)

    def post(self, request, format=None):
        data = request.data
        # check if group exists otherwise create a group
        group, created = Group.objects.get_or_create(
            name=data.get('subscription'),
            description=data.get('description')
        )
        frequency = data.get('frequency')
        # for each entry, create a new subscription entry
        for i in data:
            contact_name = i.get('contact')
            amount = i.get('amount')
            # TODO: @rhnvrm: apply the amount hack here
            contact = Contact.objects.get_instance(contact_name)
            if not contact:
                return Response(status=500, data=f"Invalid contact name {contact_name}")
            try:
                subscription = Subscription.objects.create(
                    group=group,
                    contact=contact,
                    amount=amount,
                    frequency=frequency
                )
            except Exception as e:
                print(f"Error while saving subscription {e}")
                return Response(status=500, data="Oops, this didn't go as expected")


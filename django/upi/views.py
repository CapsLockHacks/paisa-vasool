import json, re
from upi.models import Group, Contact, Subscription, Payment
from django.http import Http404
from decimal import Decimal
from upi.utils import nextAmount, get_settlement_status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from upi.serializers import GroupSerializer, ContactSerializer,PaymentSerializer, SubscriptionSerializer
from upi.jobs import create_and_send_url
import django_rq

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
                print(f"unable to find sub for amount: {money} in {sms}")
                continue
            except Exception as e:
                print(e)
                return Response(status=500, data="something went wrong while fetching sub")
            try:
                payment = Payment.objects.create(
                    status='complete',
                    contact = sub.contact,
                    group = sub.group,
                    amount = money,
                    cycle=sub.group.cycle
                )
            except Exception as e:
                print(f"unable to create payment {e}")
                return Response(status=400) 
            print("Updating sub status here.........")
            sub.last_payment_id = payment
            # reconcile for entire group (update cycle if all are paid)
            paid, unpaid = get_settlement_status(cycle=sub.group.cycle, group=sub.group)
            if not unpaid:
                sub.group.cycle +=1
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
                "name": "<>"
                "phone": "abc",
                "email": "email",
                "contact_id":<>,
            },
            
            ...
        ],
        "subscription": "netflix",
        "frequency": "weekly",
        "description": "hey this group is for netflix
    }

    """
    def get(self, request, format=None):
        # get all groups
        groups = Group.objects.all()
        data = []
        for group in groups:
            # get subscription data for each
            subscriptions = Subscription.objects.filter(group=group)
            for sub in subscriptions:
                subscription_id = sub.id
                created_date = sub.created_date
                contacts = []
                total_amount = 0
                for i in sub.get_subs_for_groups():
                    paid, unpaid = get_settlement_status(cycle=i.group.cycle, group=i.group)
                    settlement_status = len(unpaid) == 0
                    if i.last_payment_id:
                        settlement_date = i.last_payment_id.created_date.strftime("%d %b,%Y")
                    else:
                        settlement_date = None
                    contacts.append({
                        "name":i.contact.name,
                        "settlement_date": settlement_date,
                        "amount":i.amount,
                        "settled": i in paid
                    })
                    total_amount += i.amount 
            data.append({
                "settled":settlement_status,
                "name":sub.group.name,
                "created_date":created_date.strftime("%d %b,%Y"),
                "contacts":contacts,
                "amount":total_amount
            })
        return Response(status=200, data=data)


    def post(self, request, format=None):
        data = request.data
        # check if group exists otherwise create a group
        group = Group.objects.create(
            name=data.get('subscription'),
            description = data.get('description'),
            cycle = 0,
            frequency = data.get('frequency')
        )
        # for each entry, create a new subscription entry
        for i in data.get('splits'):
            # if contact_id, check for existing contact
            if i.get('contact_id'):
                try:
                    contact = Contact.objects.get(pk=i.get("contact_id"))
                except Contact.DoesNotExist:
                    return Response(status=400, data="Contact ID Is invalid")
            else:
                # create a contact
                contact, created = Contact.objects.get_or_create(
                    name=i.get("name"),
                    phone=i.get("phone"),
                    email=i.get("email")
                )
            # contact here should either be created or fetched already
            amount = i.get('amount')
            next_amount = nextAmount(amount)
            try:
                subscription = Subscription.objects.create(
                    group=group,
                    contact=contact,
                    amount=next_amount,
                )
            except Exception as e:
                print(f"Error while saving subscription {e}")
                return Response(status=500, data="Oops, this didn't go as expected")
            django_rq.enqueue(create_and_send_url, '{0:.2f}'.format(next_amount), contact.phone, contact.email, group.name)
        return Response(status=200, data="subscription created")

class Health(APIView):
    """
    Health check.
    """
    def get(self, request, format=None):
        return Response(status=200, data="all systems up...")

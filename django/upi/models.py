from django.db import models
from django.utils import timezone

# Group represents the fundamental unit in UPI-Collect.
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Contact represents the people added in each Group sharing a common Subscription
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=12, unique=True)
    email = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone

    def get_instance(self,name):
        try:
            contact = Contact.objects.get(name=name)
        except Contact.DoesNotExist:
            return None


# Payment represents the payment details for a particular subscription
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    status =  models.CharField(max_length=40)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=18, decimal_places=6)

    def __str__(self):
        return self.status

# Subscription represents each contact and group details
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=18, decimal_places=6, unique=True)
    payment_date = models.DateTimeField(default=timezone.now)
    last_payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    frequency = models.IntegerField(default=0, null=True)


    def __str__(self):
        return self.name

    def get_all_groups(self):
        return Subscription.objects.filter(group=self.group)


    def get_settlement_status(self):
        # fetch all contacts from a group
        subs = self.get_all_groups()
        unpaid = []
        paid = []
        for i in subs:
            payment = Payment.objects.filter(group=self.group,contact=i.contact)
            paid.append(i.contact)
        return paid,unpaid

    def is_contact_settled(self, customer):
        # returns True if customer has settled for a subscription
        paid, unpaid = self.get_settlement_status()
        for i in paid:
            if customer == i:
                return True
        return False
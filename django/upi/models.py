from django.db import models
from django.utils import timezone

# Group represents the fundamental unit in UPI-Collect.
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    frequency = models.CharField(max_length=20, null=True)
    cycle = models.IntegerField(null=False)
    cycle_updated_date = models.DateTimeField(default=timezone.now)

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

# Payment represents the payment details for a particular subscription
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    status =  models.CharField(max_length=40)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=18, decimal_places=6)
    cycle = models.IntegerField(null=False)

    def __str__(self):
        return self.status

# Subscription represents each contact and group details
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=18, decimal_places=6, unique=True)
    payment_date = models.DateTimeField(default=timezone.now)
    last_payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    def get_subs_for_groups(self):
        return Subscription.objects.filter(group=self.group)

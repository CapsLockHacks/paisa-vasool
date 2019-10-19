from django.db import models

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
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone

# Subscription represents each contact and group details
class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    last_payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Contact, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Payment represents the payment details for a particular subscription
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    status =  models.CharField(max_length=40)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    group = models.ForeignKey(Contact, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id
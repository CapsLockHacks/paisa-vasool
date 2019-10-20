from upi.models import Group, Contact, Subscription, Payment
from decimal import Decimal
COUNTER = Decimal(0.01)

def nextAmount(current_amount):
    current_amount = Decimal(current_amount)
    while 1 == 1:    
        try:
            Subscription.objects.get(amount = current_amount)
            current_amount += COUNTER
            print(f"setting sub current ammount as {current_amount}")
        except Subscription.DoesNotExist:
            print(f"breaking here with value as {current_amount}")
            break

    return current_amount


def get_settlement_status(group, cycle):
    payments = Payment.objects.filter(group=group, cycle=cycle)
    subscriptions = Subscription.objects.filter(group=group)
    paid = []
    unpaid = []
    for sub in subscriptions:
        if sub.last_payment_id in payments:
            paid.append(sub)
        else:
            unpaid.append(sub)
    return paid, unpaid

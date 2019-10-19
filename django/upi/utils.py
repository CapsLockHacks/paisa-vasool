from upi.models import Group, Contact, Subscription, Payment

COUNTER = 0.01

def nextAmount(current_amount):
    while 1 == 1:    
        try:
            Subscription.objects.get(amount = current_amount)
            current_amount += COUNTER
        except Subscription.DoesNotExist:
            break

    return current_amount



import requests
import json
import base64
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

def generateBase64UPIData(pa,pn,tn,am):
    return base64.b64encode(bytes(json.dumps({
        "pa": pa,
        "pn": pn,
        "tn": tn,
        "am": am
      }), "utf-8"))

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

def createUPILink(upi_id, name, tx_note, amount):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }
    base64_data = generateBase64UPIData(upi_id, name, tx_note, amount).decode('utf-8')
    data = {
    '{"long_url":"https://upi.link/l?d': '{'+base64_data+'}"}'
    }

    response = requests.post('https://i9ag6sj2r4.execute-api.ap-south-1.amazonaws.com/default/generateShortLink', headers=headers, data=data)

    return "https://upi.link/t/" + response.text

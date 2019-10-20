from django_rq import job
import urllib.request
import urllib.parse
import os.environ
import requests
from upi.utils import createUPILink

ADMIN_UPI_ID = "vivekr.dev@okhdfcbank"
ADMIN_NAME = "Vivek R"
SMS_SENDER_NAME = "TXTLCL"
APP_NAME = "PaisaPay"

@job
def send_sms(numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': os.environ['API_KEY_SMS'], 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    print(fr)

@job
def send_email(to_email, subject, text):
    resp = requests.post(
        "https://api.mailgun.net/v3/rohanverma.net/messages",
        auth=("api", os.environ['API_KEY_MAILGUN']),
        data={"from": "HackIO <hackio@rohanverma.net>",
              "to": [to_email],
              "subject": subject,
              "text": text})
    print(resp)

@job
def create_and_send_url(amount, phone_number, email_id, tx_note):
    upilink = createUPILink(ADMIN_UPI_ID, ADMIN_NAME, tx_note, amount)
    text_data = f"Hey, {ADMIN_NAME} has requested Rs.{amount}/- using {APP_NAME}. Goto {upilink} and complete the payment."
    send_sms(phone_number, SMS_SENDER_NAME, text_data).delay()
    if email_id != "":
        send_email(email_id, f"{APP_NAME} Collect Request", text_data).delay()

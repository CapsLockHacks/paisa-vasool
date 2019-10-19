from django_rq import job
import urllib.request
import urllib.parse
import os.environ
import requests

@job
def send_sms(apikey, numbers, sender, message):
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

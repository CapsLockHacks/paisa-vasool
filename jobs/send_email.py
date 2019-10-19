import requests
import os

API_KEY = "key-xxx"

def send_email(to_email, subject, text):
    resp = requests.post(
        "https://api.mailgun.net/v3/rohanverma.net/messages",
        auth=("api", os.environ['API_KEY_MAILGUN']),
        data={"from": "HackIO <hackio@rohanverma.net>",
              "to": [to_email],
              "subject": subject,
              "text": text})
    print(resp)

if __name__ == "__main__":
    send_email("rohanverma2004@gmail.com", "HackIO email", "Hello world")
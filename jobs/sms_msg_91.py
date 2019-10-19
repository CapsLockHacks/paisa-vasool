#!/usr/bin/env python
    
import urllib.request
import urllib.parse
import http.client

# Constants
AUTH_KEY_MESSAGE_91 = "XXXX"
SENDER = "HACKIO"

# Methods
def generateEndpoint(mobile_number, message):
    message = urllib.parse.quote_plus(message)
    return f"https://api.msg91.com/api/sendhttp.php?mobiles={mobile_number}&authkey={AUTH_KEY_MESSAGE_91}&route=4&sender={SENDER}&message={message}&country=91"

def main():
    conn = http.client.HTTPSConnection("api.msg91.com")
    conn.request("GET", generateEndpoint("XXXX", "Rohan has resquested money for Netflix subscription. Goto https://upi.link/t/ibkhz3 to complete payment"))
    res = conn.getresponse()
    status = res.status
    print("status", status)
    data = res.read()
    #log the message id
    print(data.decode("utf-8"))

if __name__ == "__main__":
    main()

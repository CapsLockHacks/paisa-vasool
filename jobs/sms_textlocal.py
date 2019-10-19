#!/usr/bin/env python
    
import urllib.request
import urllib.parse
    
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
    
resp =  sendSMS('XXXX-XXXX', '919911296253',
    'HACKIO', 'This is your message')
print (resp)


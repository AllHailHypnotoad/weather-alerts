from twilio.rest import TwilioRestClient
import os
import local_settings
import requests

ACCOUNT_SID= local_settings.ACCOUNT_SID
Auth_Token= local_settings.AUTH_TOKEN
MY_APP_SID = local_settings.MY_APP_SID
MY_CALLER_ID = local_settings.MY_CALLER_ID


# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient(ACCOUNT_SID, Auth_Token)
mes = "(\/) (*,,,*) (\/)"

message = client.sms.messages.create(body="%s" %mes,
    to="+16504551729",    # Replace with your phone number
    from_=MY_CALLER_ID) # Replace with your Twilio number
print message.sid

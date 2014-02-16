from twilio.rest import TwilioRestClient
import local_settings
#import requests

ACCOUNT_SID = local_settings.ACCOUNT_SID
Auth_Token = local_settings.AUTH_TOKEN
MY_APP_SID = local_settings.MY_APP_SID
MY_CALLER_ID = local_settings.MY_CALLER_ID
WG_API_KEY = local_settings.WG_API_KEY


# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient(ACCOUNT_SID, Auth_Token)
zoidburg = "(\/) (*,,,*) (\/)"


def sms(phone):
    mes = "There is a greater than 50% chance that it will rain in the next 5 hours"
    message = client.sms.messages.create(body="%s" %mes,
        to=phone,    # Replace with your phone number
        from_=MY_CALLER_ID) # Replace with your Twilio number
    print message.sid

if __name__ == '__main__':
    sms(zoidburg)

from twilio.rest import TwilioRestClient
import local_settings


# Your Account Sid and Auth Token from twilio.com/user/account
client = TwilioRestClient(local_settings.ACCOUNT_SID, local_settings.AUTH_TOKEN)
zoidburg = "(\/) (*,,,*) (\/)"


def sms(phone, mes):
    """This sends SMS messages, to and from_ variables come from the API
	MY_CALLER_ID is the number you are sending from and phone is the number you
	are sending to"""
    message = client.sms.messages.create(body = mes,
        to=phone,    # Replace with your phone number
        from_=local_settings.MY_CALLER_ID) # Replace with your Twilio number
    print message.sid

if __name__ == '__main__':
    sms(+16504551729, zoidburg)
	
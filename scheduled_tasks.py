from apscheduler.scheduler import Scheduler
import time
from send_sms import sms
from WUnder import forecast
from weather_app.models import *


sched = Scheduler()


@sched.interval_schedule(minutes=5)
#@sched.cron_schedule(hour='0,2,4,6,8,10,12,14,16,18,20,22')
def run_tasks():
    users = User.query.all()
    for user in users:
        last_checkin = user.get_last_checkin()
        if last_checkin:
            cur_weather = forecast(lat=last_chekin.lat, lon=last_checkin.lng)
            """
            Some bare bones logic to get started
            Grabs the next 5 prob of percip values (pop) form the weather underground
            data.  If pop is greater than or equal to 50 in the next 5 hours we will send an alert
            """
            alert = False
            for cur in cur_weather[0:4]:
                if int(cur['pop']) >= 50:
                    alert = True    
            # If it looks like there will be rain, send an sms
            # Need to modify the user class to contain phone numbers
            # Also need to modify the sms function to accept phone numbers
            # Need to condsider how we might clean up phone numbers
            if alert:
                print "Alert sent to " + user.name
                sms(user.phone)
    print "Scheduled tasks run"
    
    
sched.start()

while True:
    time.sleep(1)
    pass

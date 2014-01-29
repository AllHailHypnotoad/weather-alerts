weather-alerts
==============

Service that takes location data from foursquare check-ins and warns users if bad weather is forecast in the area.


**App Overview**

This app should be able to do the following when done.

1. Pull the location from a check-in
2. Pull the Lat and Long from this location
3. Using the Lat and Long contact NOAA
4. Get the forcast from NOAA
5. Use either Twellio or e-mail to send the forcast to you.


**Requirements**

- Python 2.7
- NOAA API
- Twillio API Library - pip install twillio
- Foursquare API Library - pip install foursquare
- Postgres / Postgis

**Installation Instructions**

-git clone repository
-cd repository folder
-virtualenv .
-. bin/activate
-pip install -r requirements.txt


**To DO (roughly in order of priority)**

- Foursquare API prototype
- NOAA Data examples
- Twilio Messaging Script
- Look into using OAuth2 to simplify login process
- Setup SQLAlchemy with a POstgresDB
- Create alert model for db
- Create alert view for flask


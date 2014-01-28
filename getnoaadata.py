import urllib2
from bs4 import BeautifulSoup
import datetime

def url_to_soup(address):
    markup = urllib2.urlopen(address).read()
    soup = BeautifulSoup(markup, "xml")
    return soup


def parse_xml(soup):
    conditions = soup.findAll('weather-conditions')
    time_values = soup.findAll('start-valid-time')
    time_values = time_values[7:]
    time = []
    weather = []
    for i in range(len(conditions)):
        time.append(time_values[i].string)
        if conditions[i].value != None:
            weather.append(conditions[i].value['weather-type'])
        else:
            weather.append(conditions[i].value)
    return time, weather


def get_noaa_data(lat, lon):
    address = 'http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen&lat=' + lat + '&lon=' + lon + '&listLatLon=&lat1=&lon1=&lat2=&lon2=&resolutionSub=&listLat1=&listLon1=&listLat2=&listLon2=&resolutionList=&endPoint1Lat=&endPoint1Lon=&endPoint2Lat=&endPoint2Lon=&listEndPoint1Lat=&listEndPoint1Lon=&listEndPoint2Lat=&listEndPoint2Lon=&zipCodeList=&listZipCodeList=&centerPointLat=&centerPointLon=&distanceLat=&distanceLon=&resolutionSquare=&listCenterPointLat=&listCenterPointLon=&listDistanceLat=&listDistanceLon=&listResolutionSquare=&citiesLevel=&listCitiesLevel=&sector=&gmlListLatLon=&featureType=&requestedTime=&startTime=&endTime=&compType=&propertyName=&product=time-series&begin=2004-01-01T00%3A00%3A00&end=2018-01-21T00%3A00%3A00&Unit=e&maxt=maxt&wx=wx&Submit=Submit'
    soup = url_to_soup(address)
    return parse_xml(soup)


if __name__ == '__main__':
    lat = str(38.99)
    lon = str(-77.01)
    time, weather = get_noaa_data(lat, lon)
    

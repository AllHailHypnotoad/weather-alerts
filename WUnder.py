import requests
import local_settings


WG_API_KEY = local_settings.WG_API_KEY


def weather_forecast(lat, long):
    search_url = "http://api.wunderground.com/api/%s/hourly/q/%s,%s.json" % (WG_API_KEY, lat, long)
    forecast_list = []
    fp = requests.get(search_url)
    forecasts = fp.json()
    for forecast in forecasts["hourly_forecast"]:
        each_forecast = {}
        each_forecast["hour"] = forecast["FCTTIME"]["civil"]
        each_forecast["condition"] = forecast["condition"]
        each_forecast["temp"] = forecast["temp"]["english"]
        each_forecast["pop"] = forecast["pop"]

        forecast_list.append(each_forecast)

    return forecast_list

if __name__ == '__main__':
    lat1 = "37.73539734"
    long1 = "-122.45811462"
    print weather_forecast(lat1, long1)

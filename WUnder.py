import requests
import local_settings


WG_API_KEY = local_settings.WG_API_KEY


def weather_forecast(zipcode):
    search_url = "http://api.wunderground.com/api/%s/hourly/q/%s.json" % (WG_API_KEY, zipcode)
    forecast_list = []
    fp = requests.get(search_url)
    forecasts = fp.json()
    for forecast in forecasts["hourly_forecast"]:
        each_forecast = {}
        each_forecast["hour"] = forecast["FCTTIME"]["civil"]
        each_forecast["condition"] = forecast["condition"]
        each_forecast["pop"] = forecast["pop"]

        forecast_list.append(each_forecast)

    return forecast_list

if __name__ == '__main__':
    print weather_forecast(94127)

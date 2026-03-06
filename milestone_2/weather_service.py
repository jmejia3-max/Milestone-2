import requests


def c_to_f(celsius):
    if celsius is None:
        return None
    return (celsius * 9/5) + 32


def kmh_to_mph(kmh):
    if kmh is None:
        return None
    return kmh * 0.621371


def get_weather(city, country, count=1, to_fahrenheit=True):

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "country": country,
        "count": count
    }

    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError("City not found")

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()

    current_weather = weather_data.get("current_weather", {})
    units = weather_data.get("current_weather_units", {})

    temp_value = current_weather.get("temperature")
    wind_value = current_weather.get("windspeed")

    temp_unit = units.get("temperature")
    wind_unit = units.get("windspeed")

    if to_fahrenheit and temp_unit == "°C":
        temp_value = c_to_f(temp_value)
        temp_unit = "°F"

    if to_fahrenheit and wind_unit == "km/h":
        wind_value = kmh_to_mph(wind_value)
        wind_unit = "mph"

    return {
        "temperature": round(temp_value, 2),
        "windspeed": round(wind_value, 2),
        "temp_unit": temp_unit,
        "wind_unit": wind_unit
    }
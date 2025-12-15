import os
import requests
from langchain_core.tools import tool
import datetime

@tool("get_weather_from_city", description="Get the weather for a given location with date and hour")
def get_weather_from_city(city: str, date: str = datetime.date.today().strftime("%Y-%m-%d"), hour: str = "15"):
    """
    Fetches the current weather for a given location using WeatherAPI.
    Args:
        location: The name of the city or location (e.g., "Santiago", "Guayaquil").
        date: The date for which to get the weather in YYYY-MM-DD format. Defaults to today.
    Returns:
        A dictionary containing weather information (temp_c, condition, humidity) or an error message.
    """
    print("City:", city, "Date:", date, "Hour:", hour)
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: WEATHER_API_KEY not found in environment variables."

    try:
        list_city = city.split(",")
        if len(list_city) > 1:
            city = list_city[0].strip()
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=es")
        data = response.json()
        latitude = data["results"][0]["latitude"]
        longitude = data["results"][0]["longitude"]
        print("Latitude:", latitude, "Longitude:", longitude)

        base_url = "http://api.weatherapi.com/v1/history.json"
        params = {
            "key": api_key,
            "q": f"{latitude},{longitude}",
            "dt": date,
            "hour": hour
        }
    
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Weather Data:", data)
        
        result = data.get("forecast", {}).get("forecastday", [])[0].get("hour", [])[0]
        # response = f"The weather in {city} is {data['current_weather']['temperature']}C with {data['current_weather']['windspeed']}km/h of wind."
        return f"The weather in {city} on {date} at {hour}:00 is {result.get('temp_c')}°C with {result.get('condition', {}).get('text')}, humidity at {result.get('humidity')}% and wind speed of {result.get('wind_kph')} kph."
    except requests.exceptions.RequestException as e:
        print(f"ERROR EN REQUEST: {e}")
        return f"Error fetching weather data: {e}"
    except (KeyError, IndexError) as e:
        print(f"ERROR EN DATA: {e}")
        return f"Error processing weather data: {e}"

tools = [get_weather_from_city]
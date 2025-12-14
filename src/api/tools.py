import os
import requests
import datetime
from langchain.tools import tool
from database.connection import get_db_connection

@tool
def get_current_weather(location: str):
    """
    Fetches the current weather for a given location using WeatherAPI.
    Args:
        location: The name of the city or location (e.g., "Santiago", "Guayaquil").
    Returns:
        A dictionary containing weather information (temp_c, condition, humidity) or an error message.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Error: WEATHER_API_KEY not found in environment variables."

    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": location,
        "aqi": "no"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        return {
            "location": data.get("location", {}).get("name"),
            "temperature_c": current.get("temp_c"),
            "condition": current.get("condition", {}).get("text"),
            "humidity": current.get("humidity"),
            "wind_kph": current.get("wind_kph")
        }
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

@tool
def query_sensor_data(sensor_type: str, days_back: int = 7):
    """
    Queries sensor data from the local database.
    Args:
        sensor_type: The type of sensor (e.g., 'humedad_suelo', 'temperatura_suelo', 'ph_suelo').
        days_back: Number of days back to query data for.
    Returns:
        A list of records or a message if no data found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)

    query = '''
        SELECT type, value, date, ubication
        FROM sensores
        WHERE type = ? AND date BETWEEN ? AND ?
        ORDER BY date ASC
    '''
    
    try:
        cursor.execute(query, (sensor_type, start_date, end_date))
        rows = cursor.fetchall()
        
        if not rows:
            return f"No data found for sensor '{sensor_type}' in the last {days_back} days."
        
        results = [dict(row) for row in rows]
        # Convert date objects to string for JSON serialization compatibility if needed
        for res in results:
            res['date'] = str(res['date'])
            
        return results
    except Exception as e:
        return f"Database error: {e}"
    finally:
        conn.close()

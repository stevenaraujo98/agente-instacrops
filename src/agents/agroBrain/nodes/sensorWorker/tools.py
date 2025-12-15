import datetime
import json
from langchain_core.tools import tool
from database.connection import get_db_connection

@tool("query_sensor_data", description="Query sensor data from the local database")
def query_sensor_data(sensor_type: str, city: str = "Guayaquil", days_back: int = 7) -> str:
    """
    Queries sensor data from the local database.
    Args:
        sensor_type: The type of sensor (e.g., 'humedad_suelo', 'temperatura_suelo', 'ph_suelo').
        city: The city/location to query data for. Defaults to "Guayaquil".
        days_back: Number of days back to query data for. Max 7 days.
    Returns:
        String with JSON data or error message.
    """
    print("Querying sensor data:", sensor_type, city, days_back)
    conn = get_db_connection()
    # Asegura que las filas se puedan convertir a dict si usas sqlite
    if hasattr(conn, 'row_factory'):
        import sqlite3
        conn.row_factory = sqlite3.Row
        
    cursor = conn.cursor()

    # --- LÓGICA DE FECHAS FIJAS ---
    end_date = datetime.date(2025, 12, 14)
    limit_date = datetime.date(2025, 12, 7)
    requested_start_date = end_date - datetime.timedelta(days=days_back-1)

    query = '''
        SELECT type, value, date, ubication
        FROM sensores
        WHERE type = ? AND date BETWEEN ? AND ? AND city = ?
        ORDER BY date ASC
    '''
    print("Executing query with params:", sensor_type, requested_start_date, end_date, city)
    
    try:
        cursor.execute(query, (sensor_type, requested_start_date.isoformat(), end_date.isoformat(), city))
        rows = cursor.fetchall()
        
        if not rows:
            return f"No data found for sensor '{sensor_type}' in the last {days_back} days."
        
        # Convertimos a dict y las fechas a string
        results = []
        for row in rows:
            r_dict = dict(row)
            r_dict['date'] = str(r_dict['date'])
            results.append(r_dict)
            
        return f"Retrieved {len(results)} records for '{sensor_type}' over the past {days_back} days: {json.dumps(results)}"

    except Exception as e:
        return f"Database error: {e}"
    finally:
        conn.close()

tools = [query_sensor_data]
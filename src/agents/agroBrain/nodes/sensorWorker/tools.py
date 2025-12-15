import datetime
from langchain_core.tools import tool
from database.connection import get_db_connection

@tool("query_sensor_data", description="Query sensor data from the local database")
def query_sensor_data(sensor_type: str, days_back: int = 7):
    """
    Queries sensor data from the local database.
    Args:
        sensor_type: The type of sensor (e.g., 'humedad_suelo', 'temperatura_suelo', 'ph_suelo').
        days_back: Number of days back to query data for. De maximo 7 dias
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

tools = [query_sensor_data]
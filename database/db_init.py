import sqlite3
import datetime
import random
from database.connection import get_db_connection

def init_db():
    """Initializes the database with the 'sensores' table and seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            value REAL NOT NULL,
            date DATE NOT NULL,
            ubication TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    # Check if data exists to avoid duplicate seeding
    cursor.execute('SELECT count(*) FROM sensores')
    count = cursor.fetchone()[0]

    if count == 0:
        print("Seeding database with initial data...")
        seed_data(cursor)
        conn.commit()
        print("Database initialized and seeded.")
    else:
        print("Database already contains data.")

    conn.close()

def seed_data(cursor):
    """Seeds the database with sample sensor data."""
    locations = ["Sector A", "Sector B", "Invernadero 1"]
    cities = ["Guayaquil", "Santiago de Chile", "Lima"]
    sensor_types = ["humedad_suelo", "temperatura_suelo", "ph_suelo"]
    
    today = datetime.date.today()
    
    # Generate data for the last 7 days
    for city in cities:
        for i in range(7):
            date = today - datetime.timedelta(days=i)
            for loc in locations:
                # Humedad suelo
                cursor.execute('''
                    INSERT INTO sensores (type, value, date, ubication, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("humedad_suelo", random.uniform(10.0, 30.0), date, loc, city)) # Low humidity
                
                # Temperatura suelo
                cursor.execute('''
                    INSERT INTO sensores (type, value, date, ubication, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("temperatura_suelo", random.uniform(15.0, 25.0), date, loc, city))

                # pH
                cursor.execute('''
                    INSERT INTO sensores (type, value, date, ubication, city)
                    VALUES (?, ?, ?, ?, ?)
                ''', ("ph_suelo", random.uniform(6.0, 7.5), date, loc, city))

if __name__ == "__main__":
    init_db()

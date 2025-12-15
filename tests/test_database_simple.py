"""
Test sencillo para verificar la base de datos
"""
import os
import sys
import tempfile

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.connection import get_db_connection
from database.db_init import init_db


def test_database_exists():
    """Test básico: verificar que la base de datos se puede crear"""
    # Crear una BD temporal para el test
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test.db')
    
    # Patch temporalmente la ruta de la BD
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Inicializar la BD
        init_db()
        
        # Verificar que se puede conectar
        conn = get_db_connection()
        assert conn is not None
        
        # Verificar que la tabla existe
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sensores'")
        table = cursor.fetchone()
        assert table is not None
        
        conn.close()
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        # Restaurar la ruta original
        database.connection.DB_PATH = original_path


def test_database_has_data():
    """Test básico: verificar que la BD tiene datos"""
    # Usar BD temporal
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_data.db')
    
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Crear BD con datos
        init_db()
        
        # Verificar que hay datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sensores")
        count = cursor.fetchone()[0]
        
        assert count > 0, "La base de datos debería tener datos"
        
        conn.close()
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        database.connection.DB_PATH = original_path


def test_sensor_query_tool():
    """Test básico: verificar que la herramienta de consulta funciona"""
    from src.agents.agroBrain.nodes.sensorWorker.tools import query_sensor_data
    
    # Usar BD temporal
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_query.db')
    
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Crear BD
        init_db()
        
        # Probar la consulta
        result = query_sensor_data.invoke({
            "sensor_type": "humedad_suelo", 
            "city": "Guayaquil", 
            "days_back": 7
        })
        
        # Verificar que devuelve un string
        assert isinstance(result, str)
        
        # Verificar que contiene información esperada
        assert "Retrieved" in result or "No data found" in result
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        database.connection.DB_PATH = original_path


def test_range_sensor_query_tool():
    """Test básico: verificar que la herramienta de consulta funciona"""
    from src.agents.agroBrain.nodes.sensorWorker.tools import query_sensor_data
    
    # Usar BD temporal
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_query.db')
    
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Crear BD
        init_db()
        
        # Probar la consulta
        count = 4
        result = query_sensor_data.invoke({
            "sensor_type": "humedad_suelo", 
            "city": "Guayaquil", 
            "days_back": count
        })
        
        # Verificar que devuelve un string
        assert isinstance(result, str)
        
        # Verificar que contiene información esperada
        assert "Retrieved" in result or "No data found" in result

        # Si hay datos, verificar que la cantidad de fechas coincida con count
        if "Retrieved" in result:
            import json
            
            # Extraer la parte JSON del resultado
            json_start = result.find('[')
            json_end = result.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_part = result[json_start:json_end]
                data = json.loads(json_part)
                
                # Contar fechas únicas
                fechas_unicas = set()
                for record in data:
                    fechas_unicas.add(record['date'])
                
                # Verificar que la cantidad de fechas únicas coincide con count
                assert len(fechas_unicas) <= count, f"Esperaba máximo {count} fechas únicas, pero encontré {len(fechas_unicas)}"
                print(f"✓ Verificado: {len(fechas_unicas)} fechas únicas encontradas (máximo esperado: {count})")

        
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        database.connection.DB_PATH = original_path
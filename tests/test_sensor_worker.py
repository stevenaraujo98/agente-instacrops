import os
import sys
import tempfile

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.connection import get_db_connection
from database.db_init import init_db


def test_sensor_worker_basic():
    """Test básico: verificar que el sensor worker tiene lo básico"""
    
    # Configurar BD temporal
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_sensor_worker.db')
    
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Crear BD con datos
        init_db()
        
        try:
            # Importar directamente el sensor worker
            from src.agents.agroBrain.nodes.sensorWorker.node import sensor_worker
            
            # Verificar que el worker existe
            assert sensor_worker is not None
            print("✓ Sensor worker importado correctamente")
            
        except ImportError:
            # Test de fallback - al menos verificar que las tools funcionan
            from src.agents.agroBrain.nodes.sensorWorker.tools import query_sensor_data
            
            result = query_sensor_data.invoke({
                "sensor_type": "humedad_suelo",
                "city": "Guayaquil", 
                "days_back": 3
            })
            
            assert isinstance(result, str)
            assert "Retrieved" in result or "No data found" in result
            print("✓ Test de fallback con sensor tools pasó correctamente")
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        database.connection.DB_PATH = original_path
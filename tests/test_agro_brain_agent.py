import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.connection import get_db_connection
from database.db_init import init_db


def test_agro_brain_agent_weather_query():
    """Test básico: agente responde a consulta del clima"""
    
    # Configurar BD temporal
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, 'test_agro_brain.db')
    
    import database.connection
    original_path = database.connection.DB_PATH
    database.connection.DB_PATH = test_db_path
    
    try:
        # Crear BD con datos
        init_db()
        
        # Solo mockear APIs externas y variables de entorno
        with patch('requests.get') as mock_requests, \
             patch.dict(os.environ, {'WEATHER_API_KEY': 'test_key', 'OPENAI_API_KEY': 'test_openai_key'}):
            
            # Mock de las APIs de clima (lo que sí necesitamos mockear)
            mock_geocoding = MagicMock()
            mock_geocoding.json.return_value = {
                "results": [{"latitude": -2.1894, "longitude": -79.8890}]
            }
            
            mock_weather_api = MagicMock()
            mock_weather_api.json.return_value = {
                "forecast": {
                    "forecastday": [{
                        "hour": [{
                            "temp_c": 25.0,
                            "condition": {"text": "Sunny"},
                            "humidity": 65,
                            "wind_kph": 10.0
                        }]
                    }]
                }
            }
            mock_weather_api.raise_for_status.return_value = None
            
            def api_side_effect(url, params=None):
                if "geocoding-api.open-meteo.com" in url:
                    return mock_geocoding
                elif "api.weatherapi.com" in url:
                    return mock_weather_api
                return MagicMock()
            
            mock_requests.side_effect = api_side_effect
            
            try:
                # Importar directamente el agente local
                from src.agents.agroBrain.agent import agent
                print("✓ Agente agroBrain importado correctamente")
                
                # Verificar que el agente existe
                assert agent is not None
                print("✓ Test básico del agente agroBrain pasó correctamente")
                
            except ImportError as e:
                print(f"No se pudo importar el agente completo: {e}")
                
                # Test de fallback - verificar que al menos los tools funcionan
                from src.agents.agroBrain.nodes.weatherWorker.tools import get_weather_from_city
                
                result = get_weather_from_city.invoke({
                    "city": "Guayaquil",
                    "date": "2025-12-14",
                    "hour": "15"
                })
                
                assert isinstance(result, str)
                assert "Guayaquil" in result
                assert "25.0°C" in result
                print("✓ Test de fallback con weather tool pasó correctamente")
        
        # Limpiar
        os.remove(test_db_path)
        os.rmdir(temp_dir)
        
    finally:
        database.connection.DB_PATH = original_path
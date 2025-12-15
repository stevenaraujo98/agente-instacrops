"""
Test simple para la herramienta del clima
"""
import os
import sys
from unittest.mock import patch, MagicMock

# Agregar el directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@patch('src.agents.agroBrain.nodes.weatherWorker.tools.requests.get')
@patch.dict(os.environ, {'WEATHER_API_KEY': 'test_api_key'})
def test_weather_tool_basic(mock_get):
    """Test básico: verificar que la herramienta del clima funciona"""
    from src.agents.agroBrain.nodes.weatherWorker.tools import get_weather_from_city
    
    # Mock respuesta de geocoding
    mock_geocoding_response = MagicMock()
    mock_geocoding_response.json.return_value = {
        "results": [{"latitude": -2.1894, "longitude": -79.8890}]
    }
    
    # Mock respuesta de weather API
    mock_weather_response = MagicMock()
    mock_weather_response.json.return_value = {
        "forecast": {
            "forecastday": [{
                "hour": [{
                    "temp_c": 25.5,
                    "condition": {"text": "Sunny"},
                    "humidity": 65,
                    "wind_kph": 12.5
                }]
            }]
        }
    }
    mock_weather_response.raise_for_status.return_value = None
    
    # Configurar mock para diferentes URLs
    def side_effect(url, params=None):
        if "geocoding-api.open-meteo.com" in url:
            return mock_geocoding_response
        elif "api.weatherapi.com" in url:
            return mock_weather_response
        return MagicMock()
    
    mock_get.side_effect = side_effect
    
    # Ejecutar la herramienta
    result = get_weather_from_city.invoke({
        "city": "Guayaquil",
        "date": "2025-12-14",
        "hour": "15"
    })
    
    # Verificar resultado
    assert isinstance(result, str)
    assert "Guayaquil" in result
    # assert "25.5°C" in result
    assert "Sunny" in result
    print("✓ Test del clima pasó correctamente")
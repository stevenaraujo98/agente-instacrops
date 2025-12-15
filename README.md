# agente-instacrops

## Objetivo
Chatbot para conversar con agentes, que permita a un usuario (agricultor/agrónomo) consultar el estado de sus cultivos y recibir alertas inteligentes cruzando datos de:
1.  **Clima en tiempo real** (API Externa).
2.  **Sensores de campo** (Base de datos local SQLite).

## Arquitectura del proyecto
- `langgraph.json`: Configuración de LangGraph
- `.env`: Variables de entorno (API Keys)
- `README.md`: Documentación del proyecto
- `notebooks`: Notebooks de prueba
- `/src`: Lógica del agente.
- `/tests`: Pruebas unitarias

## Arquitectura (LangGraph)
1.  **Nodo Orquestador:** Recibe el input, consulta el historial y decide a qué sub-agente llamar.
2.  **Sub-agente 1 (Clima):** Usa `weatherapi`. Herramienta: `get_current_weather(lat, lon)`.
3.  **Sub-agente 2 (Sensores):** Consulta una base de datos SQLite local.
    * *Tabla:* `sensores` (id, tipo, valor, fecha, ubicacion).
    * *Herramienta:* `query_sensor_data(tipo_sensor, rango_fecha)`.
4.  **Memoria:** Implementar `MemorySaver` o `SqliteSaver` para mantener el hilo de la conversación (Checkpointer).

## Como instalarlo
### Conda y UV - Instalación de dependencias
```
conda create -n agentInstaChallenge python=3.11 openssl cryptography grpcio -y
conda activate agentInstaChallenge

conda install -c conda-forge protobuf rust pip

pip install uv

# BASE 
uv --version 

## init 
uv init 

# add dependencies 
uv add langgraph langchain langchain-openai langchain[google-genai] langchain-deepseek

# add dev dependencies
uv add "langgraph-cli[inmem]" --dev
uv add ipykernel --dev
conda install -n langgraph ipykernel --update-deps --force-reinstall
uv add grandalf --dev

```
```
# run the agent 
uv run langgraph dev 
```

```
[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]

# recompile the project
uv pip install -e .
```

## Api clima
- WEATHER_API
Endpoint:
- http://api.weatherapi.com/v1/history.json?key={{weather_api}}&q=Guayaquil&aqi=n&dt=2025-11-30&days=2&hour=15
- http://api.weatherapi.com/v1/current.json?key={{weather_api}}&q=Guayaquil&aqi=n
- http://api.weatherapi.com/v1/forecast.json?key={{weather_api}}&q=Guayaquil&aqi=n&days=5
